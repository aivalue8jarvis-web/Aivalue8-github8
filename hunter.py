import json
import requests
import xml.etree.ElementTree as ET
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

RSS_SOURCES = [
    "https://news.google.com/rss/search?q=India+B2B+business+AI+automation+opportunity&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=India+MSME+ecommerce+software+demand&hl=en-IN&gl=IN&ceid=IN:en"
]

def fetch_live_signals() -> list:
    headlines = []
    for url in RSS_SOURCES:
        try:
            res = requests.get(url, timeout=8, headers={"User-Agent": "aIValue8-Hunter/1.0"})
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                for item in root.findall(".//item")[:5]:
                    title_el = item.find("title")
                    if title_el is not None and title_el.text:
                        headlines.append(title_el.text.strip())
        except Exception:
            continue
    return headlines[:8]

def run_opportunity_scan() -> dict:
    signals = fetch_live_signals()
    signals_text = "\n".join([f"- {s}" for s in signals]) if signals else "General Indian B2B, AI Automation, Website/App & Trading market."

    prompt = f"""
    In live Indian market signals ko padho:
    {signals_text}

    aIValue8 ke liye (AI, Web/App Build, Automation, CRM, ya B2B Purchase-Sell Support) 2 sabse practical aur ethical earning opportunities nikalo.
    Reply ONLY valid JSON:
    {{
      "opportunities": [
        {{
          "title": "Short clear opportunity title",
          "category": "B2B_SERVICE or AI_AUTOMATION or TRADE_SUPPORT",
          "score": 88,
          "action_plan": "2-line practical execution plan in Hinglish"
        }}
      ]
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Global Opportunity Hunter ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw.strip())
    saved_items = []

    conn = get_connection()
    try:
        for opp in data.get("opportunities", []):
            title = opp.get("title", "").strip()
            plan = opp.get("action_plan", "").strip()
            if not title:
                continue
            if not register_unique_or_reject("OPPORTUNITY", title, title):
                continue
            gov = check_compliance("OPPORTUNITY", f"{title} | {plan}")
            if not gov["approved"]:
                continue
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO opportunities (title, category, score, action_plan, source) VALUES (%s, %s, %s, %s, %s);",
                        (title[:240], opp.get("category", "GENERAL")[:50], int(opp.get("score", 80)), plan, "live-rss-hunter")
                    )
            saved_items.append(opp)
    finally:
        conn.close()

    if saved_items:
        msg = "\n".join([f"• [{o.get('score')}/100] {o.get('title')}\n  👉 {o.get('action_plan')}" for o in saved_items])
        send_alert(f"🌍 aIValue8 OPPORTUNITY HUNTER:\n{msg}")

    return {"status": "scan_complete", "signals_analyzed": len(signals), "new_saved": len(saved_items), "opportunities": saved_items}

def generate_daily_venture() -> dict:
    prompt = """
    aIValue8 Venture Lab ke liye AAJ ka ek bilkul naya, practical, low-investment aur high-margin Indian business idea banao
    (Web/App, AI Automation, Micro-SaaS, ya B2B Purchase-Sell brokering se juda).
    Reply ONLY valid JSON:
    {
      "title": "Unique Venture Name & Idea",
      "category": "DAILY_VENTURE",
      "score": 90,
      "action_plan": "Kaise start karein, pehla client kahan se aayega aur pricing kya rakhein (Hinglish mein)"
    }
    """
    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Chief Venture Builder ho.", model=PRIMARY_MODEL, json_mode=True)
    idea = json.loads(raw.strip())
    title = idea.get("title", "Daily Venture Idea").strip()
    plan = idea.get("action_plan", "").strip()

    if not register_unique_or_reject("DAILY_VENTURE", title, title):
        return {"status": "duplicate_skipped", "title": title}

    gov = check_compliance("DAILY_VENTURE", f"{title} | {plan}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO opportunities (title, category, score, action_plan, source) VALUES (%s, %s, %s, %s, %s);",
                    (title[:240], "DAILY_VENTURE", int(idea.get("score", 85)), plan, "venture-lab")
                )
    finally:
        conn.close()

    send_alert(f"💡 aIValue8 DAILY VENTURE IDEA [{idea.get('score')}/100]:\n🚀 {title}\n\n📋 Plan:\n{plan}")
    return {"status": "created", "venture": idea}
