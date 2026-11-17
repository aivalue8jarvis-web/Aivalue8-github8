import os
import json
import urllib.parse
import requests
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")

def build_whatsapp_link(contact: str, message: str) -> str:
    digits = "".join(ch for ch in str(contact) if ch.isdigit())
    if len(digits) == 10:
        digits = "91" + digits
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}" if len(digits) >= 10 else ""

def dispatch_whatsapp_or_link(contact: str, message: str) -> dict:
    digits = "".join(ch for ch in str(contact) if ch.isdigit())
    if len(digits) == 10:
        digits = "91" + digits
    if WHATSAPP_TOKEN and WHATSAPP_PHONE_ID and len(digits) >= 11:
        url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        payload = {"messaging_product": "whatsapp", "to": digits, "type": "text", "text": {"body": message}}
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        return {"mode": "META_CLOUD_API", "status_code": res.status_code}
    return {"mode": "WA_ME_LINK", "url": build_whatsapp_link(contact, message)}

def run_buyer_seller_matchmaker() -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, lead_name, contact, lead_type, temperature, requirement FROM crm_leads ORDER BY id DESC LIMIT 20;")
            leads = cur.fetchall()
        if not leads:
            return {"status": "no_leads", "message": "CRM mein abhi leads nahi hain. Website ya /crm/add-lead se leads add karein."}

        leads_txt = "\n".join([f"- [{l['lead_type']} | {l['temperature']}] {l['lead_name']} ({l['contact']}): {l['requirement']}" for l in leads])
        prompt = f"""
        Ye CRM leads dekho:
        {leads_txt}

        Inme se Buyer aur Seller/Service match nikalo (ya kisi Buyer ke liye aIValue8 service deal banao).
        Reply ONLY valid JSON:
        {{"matches": [{{"buyer": "Name", "seller": "Name or aIValue8", "item": "Deal summary", "score": 88, "whatsapp_pitch": "Polite 2-line Hinglish WhatsApp message"}}]}}
        """
        raw = smart_generate(prompt, system_prompt="Tum aIValue8 Purchase/Sell Matchmaker ho.", model=PRIMARY_MODEL, json_mode=True)
        data = json.loads(raw)
        saved = []
        for m in data.get("matches", []):
            key_str = f"{m.get('buyer')}:{m.get('seller')}:{m.get('item')}"
            if not register_unique_or_reject("TRADE_MATCH", key_str, m.get("item", "")):
                continue
            gov = check_compliance("TRADE_MATCH", f"{m.get('item')} | {m.get('whatsapp_pitch')}")
            if not gov["approved"]:
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO trade_matches (buyer_name, seller_name, item_summary, match_score, whatsapp_pitch) VALUES (%s,%s,%s,%s,%s);",
                        (m.get("buyer"), m.get("seller"), m.get("item"), int(m.get("score", 85)), m.get("whatsapp_pitch"))
                    )
            saved.append(m)
        if saved:
            txt = "\n".join([f"🤝 {x['buyer']} ↔️ {x['seller']} ({x['score']}%)\n   Deal: {x['item']}" for x in saved])
            send_alert(f"🔄 aIValue8 TRADE MATCHMAKER:\n{txt}")
        return {"status": "matched", "new_matches": len(saved), "matches": saved}
    finally:
        conn.close()
