import re
import json
import requests
import xml.etree.ElementTree as ET
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

# Clean, direct business discovery feeds (avoiding raw breaking news redirect 404s)
LEAD_FEEDS = [
    "https://www.reddit.com/r/forhire/search.rss?q=website+OR+app+OR+automation+OR+AI&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/IndianStartups/new/.rss?limit=6",
    "https://www.reddit.com/r/developersIndia/search.rss?q=hiring+OR+freelance+OR+agency&restrict_sr=1&sort=new"
]
HEADERS = {"User-Agent": "aIValue8-LeadHunter/2.1 (+https://sarahics.in)"}
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
            for el in entries[:4]:
                title = (el.findtext("title") or el.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
                link_el = el.find("link")
                link = (link_el.text or link_el.attrib.get("href", "")).strip() if link_el is not None else ""
                if not link:
                    al = el.find("{http://www.w3.org/2005/Atom}link")
                    if al is not None:
                        link = al.attrib.get("href", "").strip()
                desc = (el.findtext("description") or el.findtext("{http://www.w3.org/2005/Atom}content") or "")[:450]
                email = _extract_public_email(desc)
                if title and "http" in link and "news.google.com" not in link:
                    posts.append({"title": title[:170], "link": link[:210], "email": email, "snippet": re.sub("<[^>]+>", " ", desc)[:220]})
        except Exception:
            continue
    return posts[:10]

def hunt_public_leads() -> dict:
    posts = _fetch_public_posts()
    if not posts:
        return {"status": "no_feed_signals", "new_leads": 0}

    prompt = f"""
    In direct public client requirement posts ko dekho:
    {json.dumps(posts, ensure_ascii=False)}

    Inme se max 3 aisi verified leads nikalo jinka direct link ya email available ho aur jinhe Web/App, AI Automation, ya Virtual Office chahiye. News ya articles mat chunna, sirf direct looking-for-service posts chunna.
    Reply ONLY JSON:
    {{"leads": [{{"lead_name": "Name or Startup", "contact": "email if found else direct post link", "lead_type": "BUYER or EMPLOYER", "temperature": "HOT or WARM", "requirement": "2 line summary + clean link"}}]}}
    """
    data = json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 Direct Client Hunter ho.", model=PRIMARY_MODEL, json_mode=True))
    saved = []
    conn = get_connection()
    try:
        for ld in data.get("leads", []):
            name = (ld.get("lead_name") or "").strip()
            contact = (ld.get("contact") or "").strip()
            req = (ld.get("requirement") or "").strip()
            if not name or not contact or "news.google.com" in contact:
                continue
            if not register_unique_or_reject("CRM_LEAD", contact, name):
                continue
            gov = check_compliance("LEAD_HUNTER", f"{name} | {req}")
            if not gov["approved"]:
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO crm_leads (lead_name,contact,lead_type,temperature,requirement,source) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (contact) DO NOTHING;",
                        (name[:140], contact[:95], (ld.get("lead_type") or "BUYER").upper()[:25], (ld.get("temperature") or "WARM").upper()[:15], req, "direct-board-hunter")
                    )
            saved.append(ld)
    finally:
        conn.close()

    if saved:
        msg = "\n".join([f"🎯 [{x.get('lead_type')}] {x.get('lead_name')}\n   📌 {x.get('contact')}\n   💡 {x.get('requirement')[:130]}" for x in saved])
        send_alert(f"🕵️‍♂️ VERIFIED DIRECT LEADS FOUND ({len(saved)}):\n{msg}")
    return {"status": "lead_hunt_complete", "posts_scanned": len(posts), "new_leads": len(saved), "leads": saved}
