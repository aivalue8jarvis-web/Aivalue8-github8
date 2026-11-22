import os
import json
from database import get_connection
from sentinel import smart_generate, send_alert, DIAGNOSE_AND_ALERT, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject
from reel_studio import create_reel_mp4
from social_publisher import send_telegram_video

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

TOPICS_ROTATION = [
    "ATS Resume & Cover Letter for Rs 29 to clear job interviews instantly",
    "Local Shop Mini-Website and WhatsApp QR Menu for Rs 99",
    "Digital Virtual Office SaaS software with GPS attendance for remote teams",
    "Account Head CA AI for automated tax ledger preparation and compliance",
    "Autonomous AI Business OS to scale B2B trade and growth without human staff"
]

def generate_daily_batch_reels() -> dict:
    """Generates 3 distinct viral reels for the day and delivers them directly to Telegram."""
    conn = get_connection()
    generated_reels = []
    try:
        # Pick 3 different rotating topics
        for idx, topic in enumerate(TOPICS_ROTATION[:3]):
            prompt = f"""
            Topic angle: "{topic}"
            Platform: "Instagram Reels & YouTube Shorts"
            aIValue8 Corporation (Website: {PUBLIC_URL}) ke liye ek viral marketing video script banao. 
            CTA mein hamesha {PUBLIC_URL} bolna. Caption mein 8 trending Indian business hashtags aur @ai.visionoflife mention do.
            Reply ONLY valid JSON:
            {{"title":"Catchy Title {idx+1}","hook":"3-sec bold Hinglish hook","script_body":"3-4 short crisp Hinglish sentences for voiceover","caption":"Engaging caption with hashtags"}}
            """
            try:
                raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Chief Creative Director ho.", model=PRIMARY_MODEL, json_mode=True)
                data = json.loads(raw)
            except Exception:
                data = {
                    "title": f"Smart Growth #{idx+1}",
                    "hook": "Kya aapka business abhi bhi purane tarike se chal raha hai?",
                    "script_body": "aIValue8 ke sath apna business automate karo! Website, app, CRM aur instant tools ab sirf chote daamo mein. Aaj hi visit karein sarahics.in!",
                    "caption": "Transform your brand with aIValue8! 🚀 Visit https://sarahics.in today! #BusinessAutomation #StartupIndia #VirtualOffice #MakeInIndia"
                }

            title = data.get("title", f"Reel {idx+1}").strip()
            if not register_unique_or_reject("DAILY_REEL", title, title):
                continue

            # Render the MP4 video using our reel studio
            mp4 = create_reel_mp4(title, data.get("hook", ""), data.get("script_body", ""), PUBLIC_URL)
            full_caption = f"🎬 {title}\n\n{data.get('hook', '')}\n\n{data.get('caption', '')}\n\n👉 Visit: {PUBLIC_URL}"
            
            # Send directly to Telegram
            tg_res = send_telegram_video(mp4, full_caption)
            generated_reels.append({"title": title, "telegram_sent": tg_res.get("sent", False)})
            
        send_alert(f"🎬 DAILY BATCH REELS READY ({len(generated_reels)} Videos):\nJarvis ne aapke Telegram par 3 naye ready-to-post reels bhej diye hain!")
        return {"status": "batch_reels_generated", "count": len(generated_reels), "reels": generated_reels}
    finally:
        conn.close()
