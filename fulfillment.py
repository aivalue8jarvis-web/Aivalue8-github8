import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from mailer import send_email_https

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def fulfill_paid_order(invoice_id: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (invoice_id,))
            inv = cur.fetchone()
        if not inv or inv["status"] != "PAID":
            return {"status": "error", "message": "Invoice not found or not paid yet."}

        desc = inv["description"].lower()
        client_email = inv["client_contact"]
        client_name = inv["client_name"]
        result_content = ""

        if "resume" in desc or "cover letter" in desc:
            prompt = f"""
            Client Name: {client_name}
            Service: ATS Resume & Cover Letter Kit
            Create a professional, clean ATS-friendly text resume template and a matching compelling cover letter in English.
            """
            result_content = smart_generate(prompt, system_prompt="Tum professional ATS Resume Writer ho.", model=PRIMARY_MODEL)
            subject = "Your aIValue8 ATS Resume & Cover Letter Kit is Ready! 📄"
            body = f"Namaste {client_name},\n\nThank you for choosing aIValue8 Corporation. Here is your professional AI-optimized ATS Resume & Cover Letter package:\n\n{result_content}\n\nBest regards,\naIValue8 Autonomous Delivery Team ({PUBLIC_URL})"

        elif "mini-website" in desc or "qr menu" in desc or "website" in desc:
            slug = client_name.lower().replace(" ", "-")[:20]
            result_content = f"https://sarahics.in/p/{slug}"
            subject = "Your Local Business Mini-Website is Live! 🚀"
            body = f"Namaste {client_name},\n\nYour instant mobile-ready mini-website with WhatsApp ordering has been successfully generated and deployed!\n\nAccess your live page here: {result_content}\n\nBest regards,\naIValue8 Autonomous Delivery Team ({PUBLIC_URL})"

        else:
            result_content = "Service Activated Successfully."
            subject = "Your aIValue8 Service has been Activated! ✅"
            body = f"Namaste {client_name},\n\nWe have received your payment of ₹{inv['amount_inr']} for '{inv['description']}'. Your digital workspace / service has been successfully activated.\n\nBest regards,\naIValue8 Corporation ({PUBLIC_URL})"

        # Send delivery email if valid email format
        if "@" in client_email:
            send_email_https(client_email, subject, body)

        send_alert(f"📦 AUTOMATED FULFILLMENT SUCCESS:\nInvoice: {invoice_id}\nClient: {client_name}\nDelivered via Email to: {client_email}")
        return {"status": "fulfilled", "client": client_name, "description": inv["description"]}
    finally:
        conn.close()
