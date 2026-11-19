import os
import json
from database import get_connection
from sentinel import smart_generate, send_alert, diagnose_and_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject
from reel_studio import create_reel_mp4
from social_publisher import publish_or_deliver_reel

PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL", "https://sarahics.in").rstrip("/")

def generate_media_campaign(topic: str = "", platform: str = "Instagram Reels & YouTube Shorts") -> dict:
    focus = topic.strip() or "How aIValue8 automates business growth, websites/apps, WhatsApp CRM and B2B trade in India"
    prompt = f"""
    Topic: "{focus}" | Platform: "{platform}"
    aIValue8 Corporation (Website: {PUBLIC_URL}) ke liye ek viral marketing campaign banao (ASCI & ethical Indian rules ke hisaab se, CTA mein hamesha {PUBLIC_URL} bolna, aIValue8.com mat likhna).
    Reply ONLY valid JSON:
    {{"title":"Unique title","hook":"3-sec bold Hinglish hook","script_body":"3-4 short crisp Hinglish sentences for voiceover","caption":"Social caption with 5 hashtags","visual_prompt":"Short thumbnail prompt"}}
    """
    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Chief Creative Director ho.", model=PRIMARY_MODEL, json_mode=True)
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

    publish_res = {}
    try:
        mp4 = create_reel_mp4(title, data.get("hook", ""), data.get("script_body", ""), PUBLIC_URL)
        full_caption = f"{data.get('hook', '')}\n\n{data.get('caption', '')}\n\n👉 Visit: {PUBLIC_URL}"
        publish_res = publish_or_deliver_reel(mp4, full_caption)
        if publish_res.get("instagram", {}).get("published"):
            send_alert(f"📸 INSTAGRAM REEL AUTO-PUBLISHED! ✅\n📌 {title}")
    except Exception as e:
        diagnose_and_alert("media.reel_render", e)
        publish_res = {"error": str(e)}

    return {"status": "created", "campaign": data, "delivery": publish_res}
