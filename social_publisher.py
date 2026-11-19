import os
import time
import requests
from sentinel import send_alert

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def send_telegram_video(mp4_path: str, caption: str) -> dict:
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid or not os.path.exists(mp4_path):
        return {"sent": False}
    with open(mp4_path, "rb") as vf:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendVideo",
            data={"chat_id": cid, "caption": caption[:950]},
            files={"video": vf},
            timeout=60
        )
    return {"sent": r.status_code == 200, "status_code": r.status_code}

def _ig_host_and_id(token: str, ig_id: str):
    if token.startswith("IG"):
        base = "https://graph.instagram.com/v21.0"
        if not ig_id:
            me = requests.get(f"{base}/me", params={"fields": "user_id,username", "access_token": token}, timeout=15).json()
            ig_id = str(me.get("user_id") or me.get("id") or "")
        return base, ig_id
    return "https://graph.facebook.com/v21.0", ig_id

def publish_reel_to_instagram(video_url: str, caption: str) -> dict:
    ig_id = os.getenv("INSTAGRAM_USER_ID", "").strip()
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
    if not token:
        return {"published": False, "mode": "TELEGRAM_ONLY_NO_IG_TOKEN"}

    base, ig_id = _ig_host_and_id(token, ig_id)
    if not ig_id:
        return {"published": False, "error": "Instagram User ID nahi mila"}

    r1 = requests.post(
        f"{base}/{ig_id}/media",
        data={"media_type": "REELS", "video_url": video_url, "caption": caption[:2100], "share_to_feed": "true", "access_token": token},
        timeout=20
    ).json()

    cid = r1.get("id")
    if not cid:
        send_alert(f"⚠️ IG Reel Upload Error:\n{r1}")
        return {"published": False, "error": r1}

    for _ in range(18):
        time.sleep(4)
        st = requests.get(f"{base}/{cid}", params={"fields": "status_code", "access_token": token}, timeout=15).json()
        code = st.get("status_code")
        if code == "FINISHED":
            r2 = requests.post(f"{base}/{ig_id}/media_publish", data={"creation_id": cid, "access_token": token}, timeout=20).json()
            if "id" not in r2:
                send_alert(f"⚠️ IG Publish Error:\n{r2}")
            return {"published": "id" in r2, "instagram_response": r2}
        if code == "ERROR":
            send_alert(f"⚠️ IG Processing Error:\n{st}")
            return {"published": False, "error": st}
    return {"published": False, "error": "IG processing timeout"}

def publish_or_deliver_reel(mp4_path: str, caption: str) -> dict:
    fname = os.path.basename(mp4_path)
    video_url = f"{PUBLIC_URL}/media/{fname}"
    tg_res = send_telegram_video(mp4_path, f"🎬 Auto-Generated Reel Ready!\n🔗 {video_url}\n\n{caption[:600]}")
    ig_res = publish_reel_to_instagram(video_url, caption)
    return {"video_url": video_url, "telegram": tg_res, "instagram": ig_res}
