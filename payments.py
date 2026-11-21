import os
import json
import html
import secrets
import requests
import urllib.parse
from decimal import Decimal
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import send_alert
from governance import check_compliance
from treasury import record_and_distribute_earning

RAZORPAY_UPGRADE_TARGET = Decimal("25000.00")

def get_payment_config() -> dict:
    return {
        "mode": os.getenv("PAYMENT_MODE", "DIRECT_BANK").upper(),
        "upi_id": os.getenv("MERCHANT_UPI_ID", "").strip(),
        "merchant_name": os.getenv("MERCHANT_NAME", "aIValue8 Corporation").strip(),
        "bank_name": os.getenv("BANK_NAME", "").strip(),
        "acc_name": os.getenv("BANK_ACCOUNT_NAME", "").strip(),
        "acc_no": os.getenv("BANK_ACCOUNT_NO", "").strip(),
        "ifsc": os.getenv("BANK_IFSC", "").strip(),
    }

def _send_tg_payment_approval(inv_id: str, client: str, amt, utr: str):
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        return
    msg = (
        f"🔔 PAYMENT APPROVAL REQUIRED!\n"
        f"Invoice: {inv_id}\nClient: {client}\nAmount: ₹{amt}\nUTR: {utr}\n\n"
        f"Bank app check karke neeche button dabayein:"
    )
    markup = {"inline_keyboard": [[
        {"text": "✅ Accept & Split", "callback_data": f"pay_accept:{inv_id}"},
        {"text": "❌ Reject (With Reason)", "callback_data": f"pay_reject:{inv_id}"}
    ]]}
    requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": msg, "reply_markup": markup}, timeout=10)

def create_invoice(client_name: str, client_contact: str, description: str, amount_inr: float) -> dict:
    if amount_inr <= 0:
        raise ValueError("Amount 0 se zyada hona chahiye.")
    gov = check_compliance("INVOICE_CREATE", f"{client_name} | {description} | INR {amount_inr}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}
    cfg = get_payment_config()
    inv_id = "AV8-" + secrets.token_hex(3).upper()
    amt = Decimal(str(amount_inr)).quantize(Decimal("0.01"))
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO invoices (invoice_id, client_name, client_contact, description, amount_inr, payment_mode) VALUES (%s,%s,%s,%s,%s,%s);",
                    (inv_id, client_name, client_contact, description, amt, cfg["mode"])
                )
    finally:
        conn.close()
    return {"status": "created", "invoice_id": inv_id, "pay_path": f"/pay/{inv_id}", "amount_inr": float(amt), "mode": cfg["mode"]}

def get_invoice(invoice_id: str):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (invoice_id,))
            return cur.fetchone()
    finally:
        conn.close()

def submit_utr_proof(invoice_id: str, utr_number: str) -> dict:
    utr = utr_number.strip()
    if len(utr) < 6 or len(utr) > 40:
        raise ValueError("Sahi 6-40 character ka UTR / Transaction ID daalein.")
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (invoice_id,))
                inv = cur.fetchone()
                if not inv:
                    raise ValueError("Invoice nahi mili.")
                if inv["status"] == "PAID":
                    return {"status": "already_paid"}
                cur.execute("UPDATE invoices SET utr_number = %s, status = 'VERIFYING', rejection_reason = NULL WHERE invoice_id = %s;", (utr, invoice_id))
        _send_tg_payment_approval(invoice_id, inv["client_name"], inv["amount_inr"], utr)
        return {"status": "verifying", "invoice_id": invoice_id, "utr": utr}
    finally:
        conn.close()

def approve_and_settle_invoice(invoice_id: str) -> dict:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (invoice_id,))
                inv = cur.fetchone()
                if not inv:
                    raise ValueError("Invoice nahi mili.")
                if inv["status"] == "PAID":
                    return {"status": "already_paid", "invoice_id": invoice_id}
                cur.execute("UPDATE invoices SET status = 'PAID', paid_at = CURRENT_TIMESTAMP WHERE invoice_id = %s;", (invoice_id,))
        split_res = record_and_distribute_earning(invoice_id, float(inv["amount_inr"]), f"Invoice: {inv['client_name']}")
        try:
            from fulfillment import fulfill_paid_order
            fulfill_paid_order(invoice_id)
        except Exception as fe:
            print(f"Fulfillment error: {fe}")

        with conn.cursor() as cur2:
            cur2.execute("SELECT COALESCE(SUM(gross_amount_inr), 0) FROM treasury_ledger;")
            total_rev = Decimal(str(cur2.fetchone()[0]))
        cfg = get_payment_config()
        if cfg["mode"] == "DIRECT_BANK" and total_rev >= RAZORPAY_UPGRADE_TARGET:
            send_alert(f"🏦 RAZORPAY UPGRADE REMINDER! Total revenue ₹{total_rev} cross ho gaya hai.")
        return {"status": "settled", "invoice_id": invoice_id, "treasury": split_res}
    finally:
        conn.close()

def reject_invoice(invoice_id: str, reason: str) -> dict:
    clean_reason = (reason or "UTR verify nahi hua").strip()[:300]
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (invoice_id,))
                inv = cur.fetchone()
                if not inv:
                    raise ValueError("Invoice nahi mili.")
                if inv["status"] == "PAID":
                    return {"status": "already_paid", "message": "Paid invoice reject nahi ho sakti."}
                cur.execute("UPDATE invoices SET status = 'REJECTED', rejection_reason = %s WHERE invoice_id = %s;", (clean_reason, invoice_id))
        send_alert(f"❌ PAYMENT REJECTED\nInvoice: {invoice_id}\nClient: {inv['client_name']}\nReason: {clean_reason}")
        return {"status": "rejected", "invoice_id": invoice_id, "reason": clean_reason}
    finally:
        conn.close()

def render_invoice_html(inv: dict) -> str:
    cfg = get_payment_config()
    inv_id, client = html.escape(inv["invoice_id"]), html.escape(inv["client_name"])
    desc, status = html.escape(inv["description"]), html.escape(inv["status"])
    rej = html.escape(inv.get("rejection_reason") or "")
    amt = f"{float(inv['amount_inr']):.2f}"
    upi_uri = f"upi://pay?pa={urllib.parse.quote(cfg['upi_id'])}&pn={urllib.parse.quote(cfg['merchant_name'])}&am={amt}&cu=INR&tn={urllib.parse.quote(inv['invoice_id'])}" if cfg["upi_id"] else ""

    bank_html = ""
    if cfg["acc_no"] and cfg["ifsc"]:
        bank_html = f"<div class='box'><h3>🏦 Bank Transfer (IMPS/NEFT)</h3><p><b>Bank:</b> {html.escape(cfg['bank_name'])}</p><p><b>Name:</b> {html.escape(cfg['acc_name'])}</p><p><b>A/C:</b> {html.escape(cfg['acc_no'])}</p><p><b>IFSC:</b> {html.escape(cfg['ifsc'])}</p></div>"

    if status == "PAID":
        body = "<div class='paid'>✅ PAYMENT VERIFIED &amp; RECEIVED. DHANYAWAD!</div>"
    elif status == "VERIFYING":
        body = f"<div class='warn'>⏳ UTR ({html.escape(inv.get('utr_number') or '')}) submit ho gaya hai. Owner verify kar rahe hain!</div>"
    else:
        rej_box = f"<div class='err'>❌ Pichhla proof reject hua: {rej}. Sahi UTR dubara daalein.</div>" if status == "REJECTED" else ""
        qr = "<div id='qrcode' style='background:#fff;padding:12px;border-radius:12px;display:inline-block;margin:10px auto;'></div>" if upi_uri else "<p style='color:#fbbf24;'>⚠️ MERCHANT_UPI_ID Render mein set karein.</p>"
        btn = f"<a class='btn' href='{html.escape(upi_uri)}'>📲 Open GPay / PhonePe / Paytm</a>" if upi_uri else ""
        cpy = f"<p style='margin-top:8px;'><b>UPI:</b> <code>{html.escape(cfg['upi_id'])}</code> <button type='button' class='mini' onclick=\"navigator.clipboard.writeText({json.dumps(cfg['upi_id'])})\">Copy</button></p>" if cfg["upi_id"] else ""
        body = f"{rej_box}<div class='box' style='text-align:center;'><h3>📱 Scan &amp; Pay via UPI (0% Fee)</h3>{qr}{btn}{cpy}</div>{bank_html}<div class='box'><h3>🧾 Pay Ke Baad UTR Number Daalein</h3><form onsubmit='submitUtr(event)'><input id='utrInput' placeholder='12-digit UTR / Ref No...' required /><button class='btn' style='width:100%;border:none;cursor:pointer;'>Submit Payment Proof</button></form><div id='utrMsg' style='margin-top:8px;font-size:13px;'></div></div>"

    return f"<!DOCTYPE html><html><head><meta charset='UTF-8'/><meta name='viewport' content='width=device-width,initial-scale=1.0'/><title>Invoice {inv_id} - aIValue8</title><link rel='icon' type='image/svg+xml' href='/icon.svg'/><script src='https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'></script><style>*{{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif;}}body{{background:#030712;color:#e2e8f0;padding:18px;}}.w{{max-width:500px;margin:0 auto;}}.box{{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:14px;}}.amt{{font-size:30px;font-weight:900;color:#34d399;margin-top:6px;}}.btn{{display:block;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;text-decoration:none;text-align:center;padding:12px;border-radius:10px;font-weight:700;margin-top:10px;}}.mini{{background:#1e293b;color:#38bdf8;border:1px solid #334155;padding:3px 8px;border-radius:6px;cursor:pointer;}}input{{width:100%;background:#020617;color:#fff;border:1px solid #334155;border-radius:8px;padding:11px;margin-bottom:10px;}}.paid{{background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#34d399;padding:16px;border-radius:12px;text-align:center;font-weight:700;}}.warn{{background:rgba(251,191,36,0.15);border:1px solid #fbbf24;color:#fbbf24;padding:16px;border-radius:12px;text-align:center;}}.err{{background:rgba(248,113,113,0.15);border:1px solid #f87171;color:#fca5a5;padding:12px;border-radius:10px;margin-bottom:12px;}}</style></head><body><div class='w'><h2 style='color:#38bdf8;margin-bottom:12px;'>aIValue8 Official Invoice ({status})</h2><div class='box'><p><b>ID:</b> {inv_id}</p><p><b>Client:</b> {client}</p><p><b>Service:</b> {desc}</p><div class='amt'>₹{amt}</div></div>{body}</div><script>const u={json.dumps(upi_uri)};if(u&&document.getElementById('qrcode')&&typeof QRCode!=='undefined')new QRCode(document.getElementById('qrcode'),{{text:u,width:185,height:185}});async function submitUtr(e){{e.preventDefault();const r=await fetch('/pay/{inv_id}/submit-utr',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{utr_number:document.getElementById('utrInput').value.trim()}})}});if(r.ok)location.reload();else document.getElementById('utrMsg').textContent=(await r.json()).detail||'Error';}}</script></body></html>"
