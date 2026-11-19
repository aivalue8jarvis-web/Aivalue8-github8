import re
import json
import requests
import xml.etree.ElementTree as ET
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

LEAD_FEEDS = [
    "https://www.reddit.com/r/forhire/search.rss?q=website+OR+app+OR+automation+OR+AI&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/IndianStartups/new/.rss?limit=6",
    "https://news.google.com/rss/search?q=India+startup+launch+OR+MSME+digital+automation&hl=en-IN&gl=IN&ceid=IN:en"
]
HEADERS = {"User-Agent": "aIValue8-LeadHunter/1.0 (+https://sarahics.in)"}
IGNORE_DOMAINS = ("reddit.com", "google.com", "noreply", "example.com", "sentry.io", "w3.org")

def _extract_public_email(text: str) -> str:
    for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or ""):
        if not any(bad in m.lower() for bad in IGNORE_DOMAINS):
            return m
    return ""

def _fetch_public_posts() -> list:
    posts = []
    for url in LEAD_FEEDS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200:
                continue
            root = ET.fromstring(r.text)
            # Support both RSS (<item>) and Atom (<entry> used by Reddit)
            entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            for el in entries[:4]:
                title = (el.findtext("title") or el.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
                link_el = el.find("link")
                link = ""
                if link_el is not None:
                    link = (link_el.text or link_el.attrib.get("href", "")).strip()
                if not link:
                    a_link = el.find("{http://www.w3.org/2005/Atom}link")
                    if a_link is not None:
                        link = a_link.attrib.get("href", "").strip()
                desc = (el.findtext("description") or el.findtext("{http://www.w3.org/2005/Atom}content") or "")[:500]
                email = _extract_public_email(desc)
                if title:
                    posts.append({"title": title[:180], "link": link[:220], "email": email, "snippet": re.sub("<[^>]+>", " ", desc)[:260]})
        except Exception:
            continue
    return posts[:10]

def hunt_public_leads() -> dict:
    posts = _fetch_public_posts()
    if not posts:
        return {"status": "no_feed_signals", "new_leads": 0}

    prompt = f"""
    Ye public internet posts/news dekho:
    {json.dumps(posts, ensure_ascii=False)}

    Inme se sirf unhi 2 logon/companies ko chuno jinhe sach mein Website/App Build, AI Automation, CRM, ya B2B Trade Support ki zaroorat ho sakti hai (hiring/for-hire posts mein sirf '[Hiring]' chuno, '[For Hire]' freelancer mat chunna!).
    Reply ONLY valid JSON:
    {{"leads": [{{"lead_name": "Name or Company", "contact": "email if present else post link", "lead_type": "BUYER or PARTNER", "temperature": "HOT or WARM or COLD", "requirement": "2 line summary + link"}}]}}
    """
    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Ethical Public Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    saved = []

    conn = get_connection()
    try:
        for ld in data.get("leads", []):
            name = (ld.get("lead_name") or "").strip()
            contact = (ld.get("contact") or "").strip()
            req = (ld.get("requirement") or "").strip()
            if not name or not contact:
                continue
            if not register_unique_or_reject("CRM_LEAD", contact, name):
                continue
            gov = check_compliance("LEAD_HUNTER", f"{name} | {req}")
            if not gov["approved"]:
                continue
            temp = (ld.get("temperature") or "WARM").upper()
            ltype = (ld.get("lead_type") or "BUYER").upper()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name,contact,lead_type,temperature,requirement,source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], ltype[:25], temp[:15], req, "ai-lead-hunter")
                    )
            saved.append(ld)
    finally:
        conn.close()

    if saved:
        msg = "\n".join([f"🎯 [{x.get('temperature')}] {x.get('lead_name')}\n   📌 {x.get('contact')}\n   💡 {x.get('requirement')[:150]}" for x in saved])
        send_alert(f"🕵️‍♂️ NEW AUTO-DISCOVERED LEADS ({len(saved)}):\n{msg}")

    return {"status": "lead_hunt_complete", "posts_scanned": len(posts), "new_leads": len(saved), "leads": saved}
