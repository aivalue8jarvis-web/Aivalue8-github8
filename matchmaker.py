import os
import json
import urllib.parse
import requests
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject
from whatsapp_bridge import send_whatsapp_cloud_message

def build_whatsapp_link(contact: str, message: str) -> str:
    digits = "".join(ch for ch in str(contact) if ch.isdigit())
    if len(digits) == 10:
        digits = "91" + digits
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}" if len(digits) >= 10 else ""

def dispatch_whatsapp_or_link(contact: str, message: str) -> dict:
    if os.getenv("WHATSAPP_TOKEN", "").strip() and os.getenv("WHATSAPP_PHONE_ID", "").strip():
        res = send_whatsapp_cloud_message(contact, message)
        if res.get("sent"):
            return {"mode": "META_CLOUD_API", "sent": True}
    return {"mode": "WA_ME_LINK", "url": build_whatsapp_link(contact, message)}

def run_buyer_seller_matchmaker() -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, lead_name, contact, lead_type, temperature, requirement FROM crm_leads ORDER BY id DESC LIMIT 20;")
            leads = cur.fetchall()
        if not leads:
            return {"status": "no_leads", "new_matches": 0}
        leads_txt = "\n".join([f"- [{l['lead_type']} | {l['temperature']}] {l['lead_name']} ({l['contact']}): {l['requirement']}" for l in leads])
        prompt = f"""
        Ye CRM leads dekho:
        {leads_txt}

        Inme se Buyer aur Seller/Service match nikalo. Reply ONLY valid JSON:
        {{"matches": [{{"buyer": "Name", "seller": "Name or aIValue8", "item": "Deal summary", "score": 88, "whatsapp_pitch": "Polite 2-line Hinglish WhatsApp message"}}]}}
        """
        data = json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 Matchmaker ho.", model=PRIMARY_MODEL, json_mode=True))
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
                    cur.execute("INSERT INTO trade_matches (buyer_name, seller_name, item_summary, match_score, whatsapp_pitch) VALUES (%s,%s,%s,%s,%s);", (m.get("buyer"), m.get("seller"), m.get("item"), int(m.get("score", 85)), m.get("whatsapp_pitch")))
            saved.append(m)
        if saved:
            txt = "\n".join([f"🤝 {x['buyer']} ↔️ {x['seller']} ({x['score']}%)\n   Deal: {x['item']}" for x in saved])
            send_alert(f"🔄 aIValue8 TRADE MATCHMAKER:\n{txt}")
        return {"status": "matched", "new_matches": len(saved), "matches": saved}
    finally:
        conn.close()

def send_hot_lead_cfo_alert(lead: dict, cfo_pricing: dict):
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        return
    contact = lead.get("contact", "")
    digits = "".join(ch for ch in str(contact) if ch.isdigit())
    wa_link = f"https://wa.me/91{digits[-10:]}" if len(digits) >= 10 else "https://sarahics.in/panel"
    msg = (
        f"🔥 HOT LEAD & CFO CLOSING BRIEF! 🔥\n\n"
        f"👤 Client: {lead.get('lead_name')}\n📞 Contact: {contact}\n"
        f"💡 Need: {lead.get('requirement')}\n\n"
        f"💹 CFO PRICING:\n"
        f"• Target Price: ₹{cfo_pricing.get('target_price', 3500)}\n"
        f"• Min Floor Price: ₹{cfo_pricing.get('floor_price', 2500)}\n"
        f"• Strategy: {cfo_pricing.get('strategy', '')}\n"
        f"• Upsell: {cfo_pricing.get('upsell', 'Virtual Office ₹49/mo')}"
    )
    markup = {"inline_keyboard": [[{"text": "💬 Open WhatsApp", "url": wa_link}, {"text": "💳 Panel", "url": "https://sarahics.in/panel"}]]}
    requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": msg, "reply_markup": markup}, timeout=10)

def evaluate_lead_with_cfo(lead_id: int):
    if not lead_id:
        return
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM crm_leads WHERE id = %s;", (lead_id,))
            lead = cur.fetchone()
        if not lead:
            return
        prompt = f"Lead: {lead['lead_name']} | Need: {lead['requirement']}. CFO ban kar Target & Floor price tay karo. Reply JSON: {{\"target_price\": 3500, \"floor_price\": 2000, \"strategy\": \"Hinglish closing line\", \"upsell\": \"Virtual Office\"}}"
        cfo_data = json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 CFO ho.", model=PRIMARY_MODEL, json_mode=True))
        send_hot_lead_cfo_alert(lead, cfo_data)
    finally:
        conn.close()
