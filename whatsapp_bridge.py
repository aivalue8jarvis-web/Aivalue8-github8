import os
import requests
from sentinel import send_alert

def _format_indian_phone(to_phone: str) -> str:
    digits = "".join(ch for ch in str(to_phone) if ch.isdigit())
    if len(digits) == 10:
        digits = "91" + digits
    return digits

def send_whatsapp_cloud_message(to_phone: str, message_text: str) -> dict:
    tok = os.getenv("WHATSAPP_TOKEN", "").strip()
    pid = os.getenv("WHATSAPP_PHONE_ID", "").strip()
    digits = _format_indian_phone(to_phone)
    if len(digits) < 11:
        return {"sent": False, "error": "Invalid phone number"}
    if not tok or not pid:
        return {"sent": False, "error": "WHATSAPP_TOKEN ya WHATSAPP_PHONE_ID Render mein missing hai"}

    url = f"https://graph.facebook.com/v21.0/{pid}/messages"
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": digits, "type": "text", "text": {"body": message_text.strip()[:4000]}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=12)
        res_json = r.json()
        if r.status_code in (200, 201):
            return {"sent": True, "response": res_json}
        send_alert(f"⚠️ WhatsApp API Error ({digits}):\n{res_json}")
        return {"sent": False, "error": res_json}
    except Exception as e:
        return {"sent": False, "error": str(e)}

def send_whatsapp_template(to_phone: str, template_name: str = "hello_world") -> dict:
    tok = os.getenv("WHATSAPP_TOKEN", "").strip()
    pid = os.getenv("WHATSAPP_PHONE_ID", "").strip()
    digits = _format_indian_phone(to_phone)
    if len(digits) < 11 or not tok or not pid:
        return {"sent": False, "error": "Phone ya Render WhatsApp keys missing hain"}
    url = f"https://graph.facebook.com/v21.0/{pid}/messages"
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": digits, "type": "template", "template": {"name": template_name, "language": {"code": "en_US"}}}
    r = requests.post(url, headers=headers, json=payload, timeout=12)
    return {"sent": r.status_code in (200, 201), "response": r.json()}
