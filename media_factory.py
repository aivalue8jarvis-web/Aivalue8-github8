import json
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

import os
PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL", "https://sarahics.in").rstrip("/")

def generate_media_campaign(topic: str = "", platform: str = "Instagram Reels & YouTube Shorts") -> dict:
    focus = topic.strip() or "How aIValue8 automates business growth, websites/apps, WhatsApp CRM and B2B trade in India"
    prompt = f"""
    Topic: "{focus}"
    Platform: "{platform}"
    aIValue8 Corporation (Website: {PUBLIC_URL}) ke liye CTA mein hamesha {PUBLIC_URL} bolna, aIValue8.com mat likhna. Ek ek high-converting viral marketing campaign banao (ASCI & ethical Indian rules ke hisaab se, koi fake guarantee nahi).
    Reply ONLY valid JSON:
    {{
      "title": "Short unique campaign title",
      "hook": "Pehle 3 second ka powerful Hinglish hook",
      "script_body": "30-second scene-by-scene Hinglish video script",
      "caption": "Engaging social media caption with 5 hashtags",
      "visual_prompt": "Detailed AI image/thumbnail prompt in English"
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Chief Creative & Marketing Director ho.", model=PRIMARY_MODEL, json_mode=True)
    data = json.loads(raw)
    title = data.get("title", "aIValue8 Campaign").strip()

    if not register_unique_or_reject("MEDIA_CAMPAIGN", title, title):
        return {"status": "duplicate_skipped", "title": title}

    gov = check_compliance("MEDIA_CAMPAIGN", f"{title} | {data.get('script_body')} | {data.get('caption')}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO media_campaigns (title, platform, hook, script_body, caption, visual_prompt) VALUES (%s,%s,%s,%s,%s,%s);",
                    (title[:190], platform[:45], data.get("hook", ""), data.get("script_body", ""), data.get("caption", ""), data.get("visual_prompt", ""))
                )
    finally:
        conn.close()

    send_alert(f"🎬 NEW MEDIA CAMPAIGN READY ({platform}):\n📌 {title}\n🔥 Hook: {data.get('hook')}\n\n📝 Script:\n{data.get('script_body')[:800]}\n\n🎨 Image Prompt:\n{data.get('visual_prompt')[:300]}")
    return {"status": "created", "campaign": data}
