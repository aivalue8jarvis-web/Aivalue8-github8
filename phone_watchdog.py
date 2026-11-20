import os
import time
import base64
import subprocess
import requests

API_URL = "https://sarahics.in/vision/evaluate"
ADMIN_KEY = os.getenv("AIVALUE8_ADMIN_KEY", "")
WATCH_FOLDERS = ["/sdcard/DCIM/Screenshots", "/sdcard/Pictures/Screenshots"]

def get_existing_files():
    seen = set()
    for folder in WATCH_FOLDERS:
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if not f.startswith(".") and f.lower().endswith((".png", ".jpg", ".jpeg")):
                    seen.add(os.path.join(folder, f))
    return seen

def speak(text):
    try:
        subprocess.run(["termux-tts-speak", text[:300]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

if not ADMIN_KEY:
    print("❌ Pehle export AIVALUE8_ADMIN_KEY='apni-key' set karein!")
    raise SystemExit(1)

seen_files = get_existing_files()
print(f"👀 aIValue8 Phone Watchdog Active! Watching {len(seen_files)} existing screenshots...")

while True:
    try:
        for folder in WATCH_FOLDERS:
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if fname.startswith(".") or not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                fpath = os.path.join(folder, fname)
                if fpath not in seen_files:
                    seen_files.add(fpath)
                    time.sleep(1)
                    if os.path.getsize(fpath) > 4 * 1024 * 1024:
                        print(f"⚠️ File badi hai (>4MB), skip: {fname}")
                        continue
                    print(f"📸 Naya Screenshot mila: {fname} -> aIValue8 ko bhej raha hoon...")
                    with open(fpath, "rb") as img:
                        b64 = base64.b64encode(img.read()).decode("utf-8")
                    mime = "image/png" if fname.lower().endswith(".png") else "image/jpeg"
                    res = requests.post(
                        API_URL,
                        headers={"x-admin-key": ADMIN_KEY},
                        json={"filename": fname, "image_base64": b64, "mime_type": mime, "note": "Mobile screenshot auto-scan"},
                        timeout=90
                    )
                    if res.status_code == 200:
                        ev = res.json().get("evaluation", {})
                        msg = ev.get("summary", "Evaluated")
                        print(f"✅ [{ev.get('eval_type')}]: {msg}")
                        speak(msg)
                    else:
                        print(f"⚠️ Server response: {res.status_code} {res.text[:120]}")
    except Exception as e:
        print(f"🔄 Watchdog error (auto-recovering): {e}")
    time.sleep(3)
