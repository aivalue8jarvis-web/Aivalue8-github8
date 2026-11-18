import os
import json
import threading
import requests
from psycopg2.extras import RealDictCursor
from google.genai import types

from database import get_connection
from sentinel import smart_generate, diagnose_and_alert, PRIMARY_MODEL
from hunter import run_opportunity_scan, generate_daily_venture
from autopilot import run_daily_autopilot
from payments import create_invoice

PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL", "https://sarahics.in").rstrip("/")

def tg_api(method: str, payload: dict = None):
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not tok:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN missing"}
    r = requests.post(f"https://api.telegram.org/bot{tok}/{method}", json=payload or {}, timeout=15)
    return r.json()

def reply_tg(chat_id: str, text: str):
    tg_api("sendMessage", {"chat_id": chat_id, "text": text[:4000]})

def activate_telegram_webhook() -> dict:
    hook_url = f"{PUBLIC_URL}/telegram/webhook"
    return tg_api("setWebhook", {"url": hook_url})

def _process_update(update: dict):
    msg = update.get("message")
    if not msg:
        return
    chat_id = str(msg.get("chat", {}).get("id", ""))
    owner_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not owner_id or chat_id != owner_id:
        reply_tg(chat_id, "⛔ Unauthorized. Only Owner Rayan can control aIValue8 OS.")
        return

    try:
        # 1. Photo / Screenshot Vision
        if msg.get("photo"):
            reply_tg(chat_id, "👁️ Screenshot/Photo analyze ho raha hai...")
            file_id = msg["photo"][-1]["file_id"]
            f_info = tg_api("getFile", {"file_id": file_id})
            f_path = f_info.get("result", {}).get("file_path", "")
            tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
            img_bytes = requests.get(f"https://api.telegram.org/file/bot{tok}/{f_path}", timeout=20).content
            note = msg.get("caption", "Telegram photo scan")
            prompt = f'Is image/bill/product ko evaluate karo. Note: {note}. Reply ONLY JSON: {{"eval_type":"BILL or PRODUCT or ERROR or IDEA","summary":"3 line crisp Hinglish evaluation","estimated_value_inr":0}}'
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

        # 2. Commands
        if text == "/start" or text == "/help":
            reply_tg(chat_id, "🤖 aIValue8 Jarvis Ready!\n\n• Koi bhi Photo/Screenshot bhejein -> Instant Evaluation\n• /status -> Wallets, Kids Box & Salary\n• /invoice Name | Amount | Service -> UPI Link\n• /autopilot -> Full Company Run\n• /scan -> Opportunity Hunt\n• /idea -> Daily Venture\n• Ya koi bhi sawal likhein!")
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

        if text.startswith("/invoice"):
            parts = [p.strip() for p in text[8:].split("|")]
            if len(parts) < 3:
                reply_tg(chat_id, "Use format:\n/invoice Rajesh | 3500 | Website Build")
                return
            inv = create_invoice(parts[0], "", parts[2], float(parts[1]))
            if inv.get("pay_path"):
                reply_tg(chat_id, f"💳 Official Invoice Ready!\nClient: {parts[0]}\nAmount: ₹{inv['amount_inr']}\n🔗 Link: {PUBLIC_URL}{inv['pay_path']}")
            else:
                reply_tg(chat_id, f"⚠️ {inv}")
            return

        if text == "/autopilot":
            reply_tg(chat_id, "🤖 Full Auto-Pilot start ho gaya hai—report 15 second mein aayegi...")
            run_daily_autopilot()
            return

        if text == "/scan":
            reply_tg(chat_id, "🌍 Market opportunities scan ho rahi hain...")
            res = run_opportunity_scan()
            if res.get("new_saved", 0) == 0:
                reply_tg(chat_id, "🌍 Scan complete: Koi naya unique item nahi mila (duplicates skipped).")
            return

        if text == "/idea":
            reply_tg(chat_id, "💡 Aaj ka naya Venture Idea ban raha hai...")
            generate_daily_venture()
            return

        # 3. Normal CEO Chat
        reply = smart_generate(text, system_prompt="Tumhara naam 'aIValue8' hai. Tum Rayan ke Autonomous Business AI CEO ho. Crisp Hinglish mein madad karo.", model=PRIMARY_MODEL)
        reply_tg(chat_id, reply)
    except Exception as e:
        diagnose_and_alert("telegram_bot", e)
        reply_tg(chat_id, f"⚠️ Error: {str(e)[:200]}")

def handle_telegram_update(update: dict):
    threading.Thread(target=_process_update, args=(update,), daemon=True).start()
    return {"ok": True}
