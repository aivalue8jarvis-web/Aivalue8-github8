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
    "https://www.reddit.com/r/developersIndia/search.rss?q=hiring+OR+freelance+OR+job&restrict_sr=1&sort=new",
    "https://news.google.com/rss/search?q=India+startup+OR+MSME+hiring+OR+digital+automation&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=India+jobs+recruitment+OR+remote+hiring+tech&hl=en-IN&gl=IN&ceid=IN:en"
]
HEADERS = {"User-Agent": "aIValue8-LeadHunter/2.0 (+https://sarahics.in)"}
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
            entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            for el in entries[:3]:
                title = (el.findtext("title") or el.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
                link_el = el.find("link")
                link = (link_el.text or link_el.attrib.get("href", "")).strip() if link_el is not None else ""
                if not link:
                    al = el.find("{http://www.w3.org/2005/Atom}link")
                    if al is not None:
                        link = al.attrib.get("href", "").strip()
                desc = (el.findtext("description") or el.findtext("{http://www.w3.org/2005/Atom}content") or "")[:450]
                if title:
                    posts.append({"title": title[:170], "link": link[:210], "email": _extract_public_email(desc), "snippet": re.sub("<[^>]+>", " ", desc)[:220]})
        except Exception:
            continue
    return posts[:12]

def hunt_public_leads() -> dict:
    posts = _fetch_public_posts()
    if not posts:
        return {"status": "no_feed_signals", "new_leads": 0}

    prompt = f"""
    In public internet posts/news ko dekho:
    {json.dumps(posts, ensure_ascii=False)}

    Inme se max 3 ethical leads nikalo jinhe Web/App, AI Automation, Virtual Office, B2B Trade ya Job/Employer matching ki zaroorat ho.
    Reply ONLY JSON:
    {{"leads": [{{"lead_name": "Name or Company", "contact": "email if found else post link", "lead_type": "BUYER or SELLER or EMPLOYER or JOB_SEEKER", "temperature": "HOT or WARM or COLD", "requirement": "2 line summary + link"}}]}}
    """
    data = json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 Multi-Industry Lead Hunter ho.", model=PRIMARY_MODEL, json_mode=True))
    saved = []
    conn = get_connection()
    try:
        for ld in data.get("leads", []):
            name = (ld.get("lead_name") or "").strip()
            contact = (ld.get("contact") or "").strip()
            req = (ld.get("requirement") or "").strip()
            if not name or not contact or not register_unique_or_reject("CRM_LEAD", contact, name):
                continue
            gov = check_compliance("LEAD_HUNTER", f"{name} | {req}")
            if not gov["approved"]:
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name,contact,lead_type,temperature,requirement,source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], (ld.get("lead_type") or "BUYER").upper()[:25], (ld.get("temperature") or "WARM").upper()[:15], req, "multi-industry-hunter")
                    )
            saved.append(ld)
    finally:
        conn.close()

    if saved:
        msg = "\n".join([f"🎯 [{x.get('lead_type')}|{x.get('temperature')}] {x.get('lead_name')}\n   📌 {x.get('contact')}\n   💡 {x.get('requirement')[:130]}" for x in saved])
        send_alert(f"🕵️‍♂️ MULTI-INDUSTRY LEADS FOUND ({len(saved)}):\n{msg}")
    return {"status": "lead_hunt_complete", "posts_scanned": len(posts), "new_leads": len(saved), "leads": saved}
