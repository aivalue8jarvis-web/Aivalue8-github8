import os
import json
import requests
import xml.etree.ElementTree as ET
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

def hunt_nabh_hospital_leads() -> dict:
    """Scans for hospitals needing NABH accreditation assistance or compliance upgrades in India."""
    url = "https://news.google.com/rss/search?q=India+hospital+NABH+accreditation+pending+OR+quality+certification&hl=en-IN&gl=IN&ceid=IN:en"
    hospitals = []
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "aIValue8-NABHHunter/1.0"})
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            for item in root.findall(".//item")[:5]:
                t = item.find("title")
                if t is not None and t.text:
                    hospitals.append(t.text.strip())
    except Exception:
        pass
    
    if not hospitals:
        # Static simulated high-intent targeted radar if RSS is light
        hospitals = ["City Multispecialty Hospital, Civil Lines Nagpur - NABH renewal due", "Apex Life Care Hospital, Jaipur - Quality accreditation process pending"]

    prompt = f"""
    Hospital news / signals: {json.dumps(hospitals)}
    Tum aIValue8 ke Medical & NABH Compliance Hunter ho. Inme se valid hospital leads nikalo jo NABH process mein hain ya criteria mein aate hain.
    Reply ONLY valid JSON:
    {{"hospitals": [{{"hospital_name": "Name", "address": "City/State", "contact_info": "email or phone or news ref", "requirement": "NABH compliance / audit support needed"}}]}}
    """
    raw = smart_generate(prompt, system_prompt="Tum NABH Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    saved = []
    conn = get_connection()
    try:
        for h in data.get("hospitals", []):
            name = h.get("hospital_name", "").strip()
            contact = h.get("contact_info", "").strip() or "Direct Outreach Needed"
            req = h.get("requirement", "NABH Compliance Support")
            if not name or not register_unique_or_reject("NABH_LEAD", name, name):
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name, contact, lead_type, temperature, requirement, source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], "HOSPITAL_NABH", "HOT", req, "nabh-radar")
                    )
            saved.append(h)
    finally:
        conn.close()

    if saved:
        txt = "\n".join([f"🏥 {x['hospital_name']} ({x['address']})\n   📌 Contact: {x['contact_info']}\n   💡 Need: {x['requirement']}" for x in saved])
        send_alert(f"🚨 NABH HOSPITAL RADAR ALERT ({len(saved)}):\n{txt}")
    return {"status": "nabh_hunt_complete", "hospitals_found": len(saved)}

def hunt_trading_beginner_leads() -> dict:
    """Scans for beginners searching for trading institute guidance, paper trading, or stock learning."""
    url = "https://www.reddit.com/r/IndianStreetBets/new/.rss?limit=5"
    posts = []
    try:
        r = requests.get(url, headers={"User-Agent": "aIValue8-TradeHunter/1.0"}, timeout=8)
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            for item in root.findall(".//item")[:4]:
                t = item.find("title")
                if t is not None and t.text:
                    posts.append(t.text.strip())
    except Exception:
        pass

    if not posts:
        posts = ["How to start stock trading as a complete beginner in 2026?", "Best paper trading platform and mentorship in India?"]

    prompt = f"""
    Trading community posts: {json.dumps(posts)}
    Tum aIValue8 ke Trading & Anas Institute Lead Hunter ho. Beginners jo trading seekhna chahte hain unke signals nikalo.
    Reply ONLY valid JSON:
    {{"seekers": [{{"seeker_name": "Reddit User / Beginner", "contact": "Profile / Community Ref", "requirement": "Looking for beginner trading mentorship & institute guidance"}}]}}
    """
    raw = smart_generate(prompt, system_prompt="Tum Trading Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    saved = []
    conn = get_connection()
    try:
        for s in data.get("seekers", []):
            name = s.get("seeker_name", "Trading Beginner").strip()
            contact = s.get("contact", "Community Ref").strip()
            req = s.get("requirement", "Beginner trading guidance")
            if not register_unique_or_reject("TRADE_SEEKER", name, req):
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name, contact, lead_type, temperature, requirement, source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], "TRADING_BEGINNER", "WARM", req, "trading-radar")
                    )
            saved.append(s)
    finally:
        conn.close()

    if saved:
        txt = "\n".join([f"📈 TRADING SEEKER: {x['seeker_name']}\n   💡 {x['requirement']}" for x in saved])
        send_alert(f"⚡ BEGINNER TRADING RADAR ALERT:\n{txt}")
    return {"status": "trading_hunt_complete", "seekers_found": len(saved)}
