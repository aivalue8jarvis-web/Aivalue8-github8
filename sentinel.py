import os
import time
import requests
from google import genai
from google.genai import types
from database import get_connection

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"
HEALING_CHAIN = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

def send_alert(message: str):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message[:4000]}, timeout=10)
        except Exception as e:
            print(f"Telegram alert fail: {e}")

def smart_generate(prompt: str, system_prompt: str = "", model: str = PRIMARY_MODEL, json_mode: bool = False) -> str:
    if not client:
        raise RuntimeError("GEMINI_API_KEY missing hai!")
    config_args = {"temperature": 0.4}
    if system_prompt:
        config_args["system_instruction"] = system_prompt
    if json_mode:
        config_args["response_mime_type"] = "application/json"
    config = types.GenerateContentConfig(**config_args)

    models_to_try = [model] + [m for m in HEALING_CHAIN if m != model]
    last_err = None
    for idx, m in enumerate(models_to_try):
        try:
            res = client.models.generate_content(model=m, contents=prompt, config=config)
            if idx > 0:
                log_incident("sentinel.smart_generate", str(last_err), f"Auto-healed using {m}", healed=True)
            txt = (res.text or "").strip()
            if json_mode and txt.startswith("```"):
                txt = txt.strip("`").removeprefix("json").strip()
            return txt
        except Exception as err:
            last_err = err
            time.sleep(1)

    log_incident("sentinel.smart_generate", str(last_err), "All models failed", healed=False)
    send_alert(f"🚨 aIValue8 SENTINEL CRITICAL:\nAll models failed.\nLast error: {last_err}")
    raise last_err

def log_incident(module: str, error_text: str, diagnosis: str = "", healed: bool = False):
    try:
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO sentinel_incidents (module, error_text, ai_diagnosis, healed) VALUES (%s, %s, %s, %s);",
                        (module, error_text[:2000], diagnosis[:2000], healed)
                    )
        finally:
            conn.close()
    except Exception as db_err:
        print(f"Sentinel DB log error: {db_err}")

def diagnose_and_alert(module: str, error_obj: Exception):
    err_str = str(error_obj)
    diagnosis = "Auto-diagnosis unavailable"
    try:
        if client:
            diagnosis = smart_generate(
                f"Module '{module}' mein ye error aaya: {err_str}. 2 line mein root cause aur fix batao.",
                system_prompt="Tum aIValue8 ke Head Sentinel ho.",
                model=FALLBACK_MODEL
            )
    except Exception:
        pass
    log_incident(module, err_str, diagnosis, healed=False)
    send_alert(f"⚠️ aIValue8 Bug [{module}]:\nError: {err_str}\n\n🔍 Diagnosis:\n{diagnosis}")
