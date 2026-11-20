import os
import json
from google.genai import types
from database import get_connection
from sentinel import smart_generate, send_alert, diagnose_and_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject
from reel_studio import create_reel_mp4, create_reel_from_screenshots
from social_publisher import publish_or_deliver_reel

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def generate_media_campaign(topic: str = "", platform: str = "Instagram Reels & YouTube Shorts") -> dict:
    focus = topic.strip() or "How aIValue8 automates business growth, Virtual Office, websites/apps, WhatsApp CRM and B2B trade in India"
    prompt = f"""
    Topic: "{focus}" | Platform: "{platform}"
    aIValue8 Corporation (Website: {PUBLIC_URL}) ke liye viral marketing campaign banao (ASCI & ethical Indian rules ke hisaab se, CTA mein hamesha {PUBLIC_URL} bolna, aIValue8.com mat likhna).
    Caption mein 8 trending Indian business hashtags aur @ai.visionoflife mention zaroor daalna.
    Reply ONLY valid JSON:
    {{"title":"Unique title","hook":"3-sec bold Hinglish hook","script_body":"3-4 short crisp Hinglish sentences for voiceover","caption":"Engaging caption with @ai.visionoflife and 8 hashtags","visual_prompt":"Short thumbnail prompt"}}
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
        full_caption = f"{data.get('hook', '')}\n\n{data.get('caption', '')}\n\n👉 Try Live: {PUBLIC_URL}"
        publish_res = publish_or_deliver_reel(mp4, full_caption)
        if publish_res.get("instagram", {}).get("published"):
            send_alert(f"📸 INSTAGRAM REEL AUTO-PUBLISHED! ✅\n📌 {title}")
    except Exception as e:
        diagnose_and_alert("media.reel_render", e)
        publish_res = {"error": str(e)}
    return {"status": "created", "campaign": data, "delivery": publish_res}

def create_app_demo_reel_from_image(image_path: str, app_note: str = "") -> dict:
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_part = types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
    prompt = f"""
    Ye meri banayi hui app/product ka screenshot hai. Note: "{app_note}".
    Iske liye Instagram Reel ka Hinglish demo content banao (Website: {PUBLIC_URL}, mention @ai.visionoflife + 8 hashtags).
    Reply ONLY valid JSON:
    {{"title":"Short App Demo Title","hook":"3-sec Hinglish hook","script_body":"2-3 crisp sentences explaining app benefits","caption":"Caption with @ai.visionoflife and 8 hashtags"}}
    """
    data = json.loads(smart_generate([prompt, img_part], system_prompt="Tum aIValue8 App Marketing Director ho.", model="gemini-3.5-flash-lite", json_mode=True))
    gov = check_compliance("APP_DEMO_REEL", f"{data.get('title')} | {data.get('script_body')}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}

    mp4 = create_reel_from_screenshots([image_path], data.get("title", "App Demo"), data.get("hook", ""), data.get("script_body", ""), PUBLIC_URL)
    full_caption = f"{data.get('hook', '')}\n\n{data.get('caption', '')}\n\n👉 Visit: {PUBLIC_URL}"
    delivery = publish_or_deliver_reel(mp4, full_caption)
    if delivery.get("instagram", {}).get("published"):
        send_alert(f"📸 APP DEMO REEL PUBLISHED TO INSTAGRAM! ✅\n📌 {data.get('title')}")
    return {"status": "published", "campaign": data, "delivery": delivery}
