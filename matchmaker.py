# Updated matchmaker & crm notification logic with CFO pricing intelligence
import os
import json
import urllib.parse
import requests
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

def send_hot_lead_cfo_alert(lead: dict, cfo_pricing: dict):
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        return
    
    contact = lead.get('contact', '')
    digits = "".join(ch for ch in str(contact) if ch.isdigit())
    wa_link = f"https://wa.me/91{digits[-10:]}" if len(digits) >= 10 else "#"

    msg = (
        f"🔥 HOT LEAD & CFO CLOSING STRATEGY ALERT! 🔥\n\n"
        f"👤 Client Name: {lead.get('lead_name')}\n"
        f"📞 Contact: {contact}\n"
        f"🏷️ Type: {lead.get('lead_type')} | Temp: {lead.get('temperature')}\n"
        f"💡 Requirement: {lead.get('requirement')}\n\n"
        f"📊 CFO / vCA PRICING & CLOSING BRIEF:\n"
        f"• Recommended Price: ₹{cfo_pricing.get('target_price', '3500')}\n"
        f"• Absolute Floor (Min Price): ₹{cfo_pricing.get('floor_price', '2500')}\n"
        f"• Closing Strategy: {cfo_pricing.get('strategy', 'Offer 3-step setup and close on value.')}\n"
        f"• Potential Upsell: {cfo_pricing.get('upsell', 'Virtual Office subscription')}"
    )
    
    markup = {"inline_keyboard": [[
        {"text": "💬 Open WhatsApp", "url": wa_link},
        {"text": "💳 Create Invoice Link", "url": f"https://sarahics.in/panel"}
    ]]}
    requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": msg, "reply_markup": markup}, timeout=10)

def evaluate_lead_with_cfo(lead_id: int):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM crm_leads WHERE id = %s;", (lead_id,))
            lead = cur.fetchone()
        if not lead:
            return
        
        prompt = f"""
        Lead Name: {lead['lead_name']}
        Requirement: {lead['requirement']}
        Type: {lead['lead_type']}
        Tum aIValue8 ke CFO aur Sales Strategist ho. Is lead ke liye ek strict pricing aur closing brief banao.
        Floor price (neeche isse kam par deal mat karna) aur Target price (jisse pehle pitch karna hai) tay karo.
        Reply ONLY JSON:
        {{"target_price": 4999, "floor_price": 3500, "strategy": "Short closing pitch in Hinglish", "upsell": "Virtual office add-on"}}
        """
        raw = smart_generate(prompt, system_prompt="Tum aIValue8 CFO ho.", model=PRIMARY_MODEL, json_mode=True)
        cfo_data = json.loads(raw)
        send_hot_lead_cfo_alert(lead, cfo_data)
    finally:
        conn.close()
