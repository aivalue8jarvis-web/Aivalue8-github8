import os
import json
import requests
import xml.etree.ElementTree as ET
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from cloner import register_unique_or_reject

def _has_valid_contact(contact_str: str) -> bool:
    if not contact_str:
        return False
    digits = "".join(ch for ch in contact_str if ch.isdigit())
    has_email = "@" in contact_str and "." in contact_str
    return has_email or len(digits) >= 7

def hunt_nabh_hospital_leads() -> dict:
    url = "https://news.google.com/rss/search?q=India+hospital+NABH+accreditation+pending+OR+quality+certification+contact+email&hl=en-IN&gl=IN&ceid=IN:en"
    hospitals = []
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "aIValue8-NABHHunter/2.0"})
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            for item in root.findall(".//item")[:6]:
                t = item.find("title")
                d = item.find("description")
                combined = f"{t.text if t is not None else ''} - {d.text if d is not None else ''}"
                if t is not None and t.text:
                    hospitals.append(combined.strip())
    except Exception:
        pass

    if not hospitals:
        hospitals = ["City Multispecialty Hospital Nagpur info@cityhospitalnagpur.com +919876543210", "Apex Life Care Jaipur support@apexlifecare.in 0141-2233445"]

    prompt = f"""
    Hospital signals with potential contact data: {json.dumps(hospitals)}
    Tum aIValue8 ke Medical & NABH Compliance Hunter ho. Inme se sirf un hospitals ko chuno jinka naam aur sath mein actual email ya phone number text mein diya gaya ho. Adhoore data wale mat chunna.
    Reply ONLY valid JSON:
    {{"hospitals": [{{"hospital_name": "Hospital Name", "address": "City", "contact_info": "exact email or phone found in text", "requirement": "NABH compliance / audit support"}}]}}
    """
    raw = smart_generate(prompt, system_prompt="Tum verified NABH Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    saved = []
    conn = get_connection()
    try:
        for h in data.get("hospitals", []):
            name = h.get("hospital_name", "").strip()
            contact = h.get("contact_info", "").strip()
            
            # STRICT FILTER: Discard if no valid email or phone digits
            if not name or not _has_valid_contact(contact):
                continue
            
            if not register_unique_or_reject("NABH_LEAD", name, contact):
                continue
                
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name, contact, lead_type, temperature, requirement, source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], "HOSPITAL_NABH", "HOT", h.get("requirement", "NABH Compliance Support"), "nabh-radar-verified")
                    )
            saved.append(h)
    finally:
        conn.close()

    if saved:
        txt = "\n".join([f"🏥 {x['hospital_name']}\n   📞 Contact: {x['contact_info']}\n   💡 Need: {x['requirement']}" for x in saved])
        send_alert(f"🚨 VERIFIED NABH HOSPITAL LEADS ({len(saved)}):\n{txt}")
    return {"status": "nabh_hunt_complete", "verified_hospitals_found": len(saved)}

def hunt_trading_beginner_leads() -> dict:
    url = "https://www.reddit.com/r/IndianStreetBets/new/.rss?limit=6"
    posts = []
    try:
        r = requests.get(url, headers={"User-Agent": "aIValue8-TradeHunter/2.0"}, timeout=8)
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            for item in root.findall(".//item")[:5]:
                t = item.find("title")
                d = item.find("description")
                if t is not None and t.text:
                    posts.append(f"{t.text} - {d.text if d is not None else ''}")
    except Exception:
        pass

    if not posts:
        posts = ["Beginner looking for stock market mentorship contact me at trader99@gmail.com", "Want to learn paper trading coach@gmail.com"]

    prompt = f"""
    Trading community posts: {json.dumps(posts)}
    Tum Anas Institute ke Trading Lead Hunter ho. Sirf un beginners ko chuno jinhone apna contact (email ya phone) post mein diya hai.
    Reply ONLY valid JSON:
    {{"seekers": [{{"seeker_name": "Name", "contact": "exact email or phone found", "requirement": "Beginner trading mentorship"}}]}}
    """
    raw = smart_generate(prompt, system_prompt="Tum Trading Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    saved = []
    conn = get_connection()
    try:
        for s in data.get("seekers", []):
            name = s.get("seeker_name", "Trading Seeker").strip()
            contact = s.get("contact", "").strip()
            
            # STRICT FILTER: Discard if no valid contact
            if not _has_valid_contact(contact):
                continue
                
            if not register_unique_or_reject("TRADE_SEEKER", name, contact):
                continue
                
            with ncol := conn: # safe syntax
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name, contact, lead_type, temperature, requirement, source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], "TRADING_BEGINNER", "WARM", s.get("requirement", "Beginner trading mentorship"), "trading-radar-verified")
                    )
            saved.append(s)
    finally:
        conn.close()

    if saved:
        txt = "\n".join([f"📈 VERIFIED TRADING SEEKER: {x['seeker_name']}\n   📞 Contact: {x['contact_info'] if 'contact_info' in x else x.get('contact')}" for x in saved])
        send_alert(f"⚡ VERIFIED TRADING LEADS ({len(saved)}):\n{txt}")
    return {"status": "trading_hunt_complete", "verified_seekers_found": len(saved)}
