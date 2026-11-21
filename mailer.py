import os
import re
import json
import requests
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from matchmaker import dispatch_whatsapp_or_link
from payments import create_invoice

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "sales@sarahics.in").strip()
GMAIL_BRIDGE_URL = os.getenv("GMAIL_BRIDGE_URL", "").strip()
PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL", "https://sarahics.in").rstrip("/")

def extract_email(text: str) -> str:
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(text or ""))
    return m.group(0) if m else ""

def send_email_https(to_email: str, subject: str, body: str) -> dict:
    footer = "\n\n---\naIValue8 Corporation (Sarahics) | AI, Web/App, Automation & Trade\nSupport: sales@sarahics.in"
    full_body = body.strip() + footer
    
    # Try Brevo API if key exists
    if BREVO_API_KEY and len(BREVO_API_KEY) > 10:
        try:
            res = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
                json={"sender": {"name": "aIValue8 Corporation", "email": SENDER_EMAIL}, "to": [{"email": to_email}], "subject": subject, "textContent": full_body},
                timeout=10
            )
            if res.status_code in (200, 201, 202):
                return {"sent": True, "mode": "BREVO_API", "code": res.status_code}
            else:
                print(f"Brevo API error response: {res.text}")
        except Exception as e:
            print(f"Brevo API exception: {e}")

    # Try Gmail Bridge if configured
    if GMAIL_BRIDGE_URL:
        try:
            res = requests.post(GMAIL_BRIDGE_URL, json={"to": to_email, "subject": subject, "body": full_body}, timeout=10)
            if res.status_code == 200:
                return {"sent": True, "mode": "GMAIL_BRIDGE", "code": 200}
        except Exception:
            pass

    # Fallback / Draft Mode (Logs cleanly to Telegram/Console instead of failing)
    print(f"⚠️ [MAIL FALLBACK] To: {to_email} | Sub: {subject}")
    return {"sent": False, "mode": "FALLBACK_LOGGED", "code": 0}

def process_crm_outreach() -> dict:
    conn = get_connection()
    actions = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM crm_leads
                WHERE outreach_stage BETWEEN 0 AND 3
                  AND (last_outreach_at IS NULL
                       OR (outreach_stage = 1 AND last_outreach_at <= NOW() - INTERVAL '2 days')
                       OR (outreach_stage = 2 AND last_outreach_at <= NOW() - INTERVAL '3 days')
                       OR (outreach_stage = 3 AND last_outreach_at <= NOW() - INTERVAL '2 days'))
                ORDER BY id DESC LIMIT 5;
            """)
            leads = cur.fetchall()

        for lead in leads:
            email = extract_email(lead["contact"]) or extract_email(lead["requirement"])
            stage = lead["outreach_stage"] or 0

            if not email or stage == 3:
                pitch = smart_generate(
                    f"Lead: {lead['lead_name']} | Need: {lead['requirement']}. 2-line polite Hinglish WhatsApp follow-up message likho.",
                    system_prompt="Tum aIValue8 Sales Closer ho.", model=PRIMARY_MODEL
                )
                gov = check_compliance("FALLBACK_OUTREACH", pitch)
                if not gov["approved"]:
                    continue
                wa_res = dispatch_whatsapp_or_link(lead["contact"], pitch)
                reason = "No Email ID" if not email else "Email No-Response (Day 7 Fallback)"
                send_alert(
                    f"📲 CHANNEL SWITCH ({reason}):\nLead: {lead['lead_name']} ({lead['contact']}) [{lead['temperature']}]\n"
                    f"💬 Message:\n{pitch}\n👉 Link: {wa_res.get('url', 'Sent via Meta API')}"
                )
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE crm_leads SET outreach_stage = 4, last_outreach_at = CURRENT_TIMESTAMP WHERE id = %s;", (lead["id"],))
                actions.append({"lead": lead["lead_name"], "channel": "WHATSAPP_FALLBACK", "reason": reason})
                continue

            stage_desc = {0: "Initial Deal Proposal", 1: "Polite Day-2 Value Follow-up", 2: "Final Day-5 Check-in"}[stage]
            raw = smart_generate(
                f"Stage: {stage_desc}. Client: {lead['lead_name']}. Need: {lead['requirement']}. Site: {PUBLIC_URL}. Reply JSON: {{\"subject\":\"short subject\",\"body\":\"4-line polite Hinglish/English business email\"}}",
                system_prompt="Tum aIValue8 B2B Email Closer ho.", model=PRIMARY_MODEL, json_mode=True
            )
            mail_data = json.loads(raw)
            gov = check_compliance("EMAIL_OUTREACH", f"{mail_data['subject']} | {mail_data['body']}")
            if not gov["approved"]:
                continue
            send_res = send_email_https(email, mail_data["subject"], mail_data["body"])
            if not send_res["sent"]:
                send_alert(f"📧 EMAIL DRAFT LOGGED ({stage_desc}):\nTo: {email}\nSub: {mail_data['subject']}\n\n{mail_data['body']}")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE crm_leads SET outreach_stage = %s, last_outreach_at = CURRENT_TIMESTAMP WHERE id = %s;", (stage + 1, lead["id"]))
            actions.append({"lead": lead["lead_name"], "channel": send_res["mode"], "stage": stage + 1})

        return {"status": "outreach_done", "processed": len(actions), "actions": actions}
    finally:
        conn.close()

def handle_email_reply(sender_email: str, subject: str, reply_text: str) -> dict:
    txt_low = reply_text.lower()
    if any(w in txt_low for w in ["stop", "unsubscribe", "do not contact", "mat bhejo"]):
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE crm_leads SET outreach_stage = -1 WHERE contact ILIKE %s;", (f"%{sender_email}%",))
        finally:
            conn.close()
        return {"status": "unsubscribed_dpdp_compliant", "email": sender_email}

    prompt = f"""
    Client ({sender_email}) ne email reply bheja: "{reply_text}"
    Agar client deal confirm kar raha hai ya price/payment maang raha hai, toh ready_to_pay=true aur estimated INR amount do.
    Reply ONLY JSON: {{"reply_body": "polite Hinglish/English reply", "ready_to_pay": false, "amount_inr": 0, "service_desc": "Service"}}
    """
    ai = json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 Deal Closer ho.", model=PRIMARY_MODEL, json_mode=True))
    reply_body = ai.get("reply_body", "Thank you for your reply!")
    if ai.get("ready_to_pay") and float(ai.get("amount_inr", 0)) > 0:
        inv = create_invoice(sender_email, sender_email, ai.get("service_desc", "aIValue8 Service"), float(ai["amount_inr"]))
        if inv.get("pay_path"):
            reply_body += f"\n\n💳 Payment & Official Invoice Link: {PUBLIC_URL}{inv['pay_path']}"
            send_alert(f"🤝 DEAL CLOSING! Invoice {inv['invoice_id']} (₹{ai['amount_inr']}) auto-generated for {sender_email}!")
    send_res = send_email_https(sender_email, f"Re: {subject}", reply_body)
    return {"status": "replied", "email_mode": send_res["mode"], "reply_body": reply_body}
