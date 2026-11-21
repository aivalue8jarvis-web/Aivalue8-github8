import os
import re
import time
import json
import threading
import requests
from psycopg2.extras import RealDictCursor
from google.genai import types

from database import get_connection
from sentinel import smart_generate, diagnose_and_alert, PRIMARY_MODEL
from lead_hunter import hunt_public_leads
from hunter import run_opportunity_scan, generate_daily_venture
from autopilot import run_daily_autopilot
from payments import create_invoice, approve_and_settle_invoice, reject_invoice
from whatsapp_bridge import send_whatsapp_cloud_message, send_whatsapp_template
from backup import run_daily_backup
from media_factory import generate_media_campaign, create_app_demo_reel_from_image
from c_suite import run_csuite_board

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def tg_api(method: str, payload: dict = None):
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not tok:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN missing"}
    return requests.post(f"https://api.telegram.org/bot{tok}/{method}", json=payload or {}, timeout=15).json()

def reply_tg(chat_id: str, text: str):
    tg_api("sendMessage", {"chat_id": chat_id, "text": text[:4000]})

def activate_telegram_webhook() -> dict:
    tg_api("setMyCommands", {"commands": [
        {"command": "status", "description": "Wallets, Kids Box & CRM Status"},
        {"command": "autopilot", "description": "Poori AI Company + C-Suite Run"},
        {"command": "csuite", "description": "COO, CFO/vCA & CSO Board Report"},
        {"command": "reel", "description": "Auto Motion-Graphics Reel Banayein"},
        {"command": "leads", "description": "Multi-Industry + Job Leads Hunt"},
        {"command": "scan", "description": "Nayi Business Opportunities Dhundhein"},
        {"command": "idea", "description": "Aaj Ka Naya Business Idea"},
        {"command": "invoice", "description": "UPI Link (/invoice Name | Amt | Work)"},
        {"command": "wa", "description": "WhatsApp (/wa Phone | Message)"},
        {"command": "watest", "description": "WhatsApp Hello Test (/watest Phone)"},
        {"command": "backup", "description": "Database Backup backup@sarahics.in"},
        {"command": "help", "description": "Jarvis Commands Cheat Sheet"}
    ]})
    return tg_api("setWebhook", {"url": f"{PUBLIC_URL}/telegram/webhook"})

def _process_update(update: dict):
    owner_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    # 1. Handle Payment Accept / Reject Inline Buttons
    cq = update.get("callback_query")
    if cq:
        cq_id = cq.get("id")
        chat_id = str(cq.get("message", {}).get("chat", {}).get("id", ""))
        data = cq.get("data", "")
        tg_api("answerCallbackQuery", {"callback_query_id": cq_id})
        if not owner_id or chat_id != owner_id:
            return
        try:
            if data.startswith("pay_accept:"):
                inv_id = data.split(":", 1)[1]
                res = approve_and_settle_invoice(inv_id)
                reply_tg(chat_id, f"✅ Invoice {inv_id} ACCEPTED & SPLIT! ({res.get('status')})")
            elif data.startswith("pay_reject:"):
                inv_id = data.split(":", 1)[1]
                tg_api("sendMessage", {
                    "chat_id": chat_id,
                    "text": f"Reject Reason for {inv_id}:\n(Is message par reply mein rejection reason likhein)",
                    "reply_markup": {"force_reply": True, "selective": True}
                })
        except Exception as e:
            reply_tg(chat_id, f"⚠️ Payment action error: {e}")
        return

    msg = update.get("message")
    if not msg:
        return
    chat_id = str(msg.get("chat", {}).get("id", ""))
    if not owner_id or chat_id != owner_id:
        reply_tg(chat_id, "⛔ Unauthorized. Only Owner Rayan can control aIValue8 OS.")
        return

    try:
        # 2. Handle Reply to Rejection Reason Box
        rep_txt = (msg.get("reply_to_message") or {}).get("text", "")
        m_rej = re.search(r"Reject Reason for (AV8-[A-Z0-9]+):", rep_txt)
        if m_rej and msg.get("text"):
            inv_id = m_rej.group(1)
            reject_invoice(inv_id, msg["text"])
            return

        # 3. Handle Photo: 'reel:' -> App Demo Video Reel | Normal -> Vision Evaluator
        if msg.get("photo"):
            file_id = msg["photo"][-1]["file_id"]
            f_path = tg_api("getFile", {"file_id": file_id}).get("result", {}).get("file_path", "")
            tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
            img_bytes = requests.get(f"https://api.telegram.org/file/bot{tok}/{f_path}", timeout=20).content
            caption = (msg.get("caption") or "").strip()

            if caption.lower().startswith("reel"):
                reply_tg(chat_id, "🎬 Aapki App Screenshot se Video Reel + Voiceover + Hashtags ban rahe hain... 15 sec!")
                os.makedirs("/tmp/aivalue8_media", exist_ok=True)
                tmp_jpg = f"/tmp/aivalue8_media/tg_app_{int(time.time())}.jpg"
                with open(tmp_jpg, "wb") as f:
                    f.write(img_bytes)
                try:
                    create_app_demo_reel_from_image(tmp_jpg, caption)
                finally:
                    if os.path.exists(tmp_jpg):
                        os.remove(tmp_jpg)
                return

            reply_tg(chat_id, "👁️ Screenshot/Photo analyze ho raha hai...")
            prompt = f'Evaluate image. Note: {caption or "Photo scan"}. Reply ONLY JSON: {{"eval_type":"BILL or PRODUCT or ERROR or IDEA","summary":"3 line crisp Hinglish evaluation","estimated_value_inr":0}}'
            img_part = types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
            ev = json.loads(smart_generate([prompt, img_part], system_prompt="Tum aIValue8 Vision Evaluator ho.", model="gemini-3.5-flash-lite", json_mode=True))
            conn = get_connection()
            try:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO vision_evaluations (filename,eval_type,summary,estimated_value_inr) VALUES (%s,%s,%s,%s);", ("tg_photo.jpg", ev.get("eval_type", "PHOTO")[:45], ev.get("summary", ""), float(ev.get("estimated_value_inr", 0))))
            finally:
                conn.close()
            reply_tg(chat_id, f"✅ [{ev.get('eval_type')}] (Est: ₹{ev.get('estimated_value_inr', 0)})\n\n{ev.get('summary')}")
            return

        text = (msg.get("text") or "").strip()
        if not text:
            return

        if text in ("/start", "/help"):
            reply_tg(chat_id, "🤖 aIValue8 Jarvis Ready!\n\n• App Screenshot + caption 'reel: detail' bhejein -> App Video Reel!\n• Normal Photo bhejein -> Vision Evaluation\n• /status -> Wallets, Kids Box & Salary\n• /autopilot -> Full Company + C-Suite\n• /csuite -> COO, CFO/vCA & CSO Board\n• /reel -> Auto Motion Reel\n• /leads -> Multi-Industry & Job Leads\n• /invoice Name | Amt | Work -> UPI Link\n• /backup -> Send DB Backup Email")
            return

        if text == "/status":
            conn = get_connection()
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT display_name, balance_inr FROM treasury_wallets ORDER BY allocation_percent DESC;")
                    ws = cur.fetchall()
                    cur.execute("SELECT COUNT(*) AS c FROM crm_leads;")
                    lc = cur.fetchone()["c"]
                    cur.execute("SELECT COUNT(*) AS c FROM agents_registry WHERE status='ACTIVE';")
                    ac = cur.fetchone()["c"]
            finally:
                conn.close()
            w_txt = "\n".join([f"• {w['display_name']}: ₹{w['balance_inr']}" for w in ws])
            reply_tg(chat_id, f"👑 aIValue8 LIVE STATUS:\n\n💰 Wallets:\n{w_txt}\n\n🧬 Active Clones: {ac} | 📋 CRM Leads: {lc}")
            return

        if text == "/leads":
            reply_tg(chat_id, "🕵️‍♂️ Multi-Industry + Job/Employer leads hunt ho rahe hain...")
            res = hunt_public_leads()
            conn = get_connection()
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT lead_name, contact, lead_type, temperature FROM crm_leads ORDER BY id DESC LIMIT 5;")
                    rows = cur.fetchall()
            finally:
                conn.close()
            lst = "\n".join([f"• [{r['lead_type']}|{r['temperature']}] {r['lead_name']} ({r['contact']})" for r in rows]) or "Koi lead nahi."
            reply_tg(chat_id, f"📋 Latest 5 Leads (New: {res.get('new_leads', 0)}):\n{lst}")
            return

        if text.startswith("/invoice"):
            parts = [p.strip() for p in text[8:].split("|")]
            if len(parts) < 3:
                reply_tg(chat_id, "Format:\n/invoice Rajesh | 3500 | Website Build")
                return
            inv = create_invoice(parts[0], "", parts[2], float(parts[1]))
            if inv.get("pay_path"):
                reply_tg(chat_id, f"💳 Invoice Ready!\nClient: {parts[0]}\nAmount: ₹{inv['amount_inr']}\n🔗 {PUBLIC_URL}{inv['pay_path']}")
            else:
                reply_tg(chat_id, f"⚠️ {inv}")
            return

        if text == "/autopilot":
            reply_tg(chat_id, "🤖 Full Auto-Pilot + C-Suite Board chal raha hai...")
            run_daily_autopilot()
            return

        if text == "/csuite":
            reply_tg(chat_id, "🏛️ COO, CFO/vCA & CSO Executive Board meeting chal rahi hai...")
            run_csuite_board()
            return

        if text == "/reel":
            reply_tg(chat_id, "🎬 Motion-Graphics Reel Video ban rahi hai... 15 sec!")
            generate_media_campaign()
            return

        if text == "/scan":
            reply_tg(chat_id, "🌍 Market opportunities scan ho rahi hain...")
            res = run_opportunity_scan()
            if res.get("new_saved", 0) == 0:
                reply_tg(chat_id, "🌍 Scan complete: Koi naya unique item nahi mila.")
            return

        if text == "/idea":
            reply_tg(chat_id, "💡 Aaj ka Venture Idea ban raha hai...")
            generate_daily_venture()
            return

        if text.startswith("/watest"):
            ph = text[7:].strip()
            if not ph:
                reply_tg(chat_id, "Use: /watest 91XXXXXXXXXX")
                return
            r = send_whatsapp_template(ph, "hello_world")
            reply_tg(chat_id, f"📱 WhatsApp Template Test: {r}")
            return

        if text.startswith("/wa "):
            parts = [x.strip() for x in text[4:].split("|", 1)]
            if len(parts) < 2:
                reply_tg(chat_id, "Use: /wa 91XXXXXXXXXX | Aapka message")
                return
            w_res = send_whatsapp_cloud_message(parts[0], parts[1])
            reply_tg(chat_id, "✅ WhatsApp sent!" if w_res.get("sent") else f"⚠️ WhatsApp Error: {w_res.get('error')}")
            return

        if text == "/backup":
            reply_tg(chat_id, "💾 Database backup bheja ja raha hai...")
            run_daily_backup()
            return

        reply = smart_generate(text, system_prompt="Tumhara naam 'aIValue8' hai. Tum Rayan ke Autonomous AI CEO ho. Crisp Hinglish mein jawab do.", model=PRIMARY_MODEL)
        reply_tg(chat_id, reply)
    except Exception as e:
        diagnose_and_alert("telegram_bot", e)
        reply_tg(chat_id, f"⚠️ Error: {str(e)[:200]}")

def handle_telegram_update(update: dict):
    threading.Thread(target=_process_update, args=(update,), daemon=True).start()
    return {"ok": True}
