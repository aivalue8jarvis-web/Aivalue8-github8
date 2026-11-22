import os
import json
from sentinel import smart_generate, PRIMARY_MODEL
from payments import create_invoice

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def generate_whatsapp_ai_reply(incoming_msg: str, sender_phone: str) -> str:
    """Generates an intelligent, polite AI sales/support response for incoming WhatsApp messages."""
    msg_low = incoming_msg.lower()
    
    # Quick intent shortcuts for micro-store items
    if "resume" in msg_low or "cv" in msg_low:
        inv = create_invoice(f"WA Client {sender_phone[-4:]}", sender_phone, "ATS Resume & Cover Letter Kit", 29.0)
        return f"Namaste! Aapka ATS Resume & Cover Letter kit ready hai (Sirf ₹29). Is secure UPI link se pay karein:\n{PUBLIC_URL}{inv['pay_path']}"
    
    if "website" in msg_low or "mini" in msg_low or "menu" in msg_low or "shop" in msg_low:
        inv = create_invoice(f"WA Client {sender_phone[-4:]}", sender_phone, "Local Shop Mini-Website & QR Menu", 99.0)
        return f"Namaste! Apni dukan ya cafe ke liye Mobile Website / QR Menu banwane ke liye (Sirf ₹99) is secure link se pay karein:\n{PUBLIC_URL}{inv['pay_path']}"

    if "office" in msg_low or "saas" in msg_low or "attendance" in msg_low:
        inv = create_invoice(f"WA Client {sender_phone[-4:]}", sender_phone, "Virtual Office Starter Desk Subscription", 49.0)
        return f"Namaste! Virtual Office Starter Desk (GPS Attendance & CRM) ke liye (Sirf ₹49/mo) is secure link se pay karein:\n{PUBLIC_URL}{inv['pay_path']}"

    # General AI Sales & Support Prompt
    prompt = f"""
    Incoming WhatsApp message from client ({sender_phone}): "{incoming_msg}"
    Tum aIValue8 Corporation ke official WhatsApp Sales & Support Assistant ho. 
    Hamaray products: ATS Resume (Rs 29), Shop Mini-Website (Rs 99), Virtual Office SaaS (Rs 49/mo).
    Client ko polite, short aur helpful Hinglish mein jawab do aur unhe sarahics.in/store par guide karo.
    Reply ONLY the reply text message (no json).
    """
    reply = smart_generate(prompt, system_prompt="Tum WhatsApp AI sales closer ho.", model=PRIMARY_MODEL)
    return reply.strip()
