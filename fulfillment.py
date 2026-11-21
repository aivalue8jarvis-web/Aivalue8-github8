import os
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
            return {"status": "error", "message": "Invoice paid nahi hai."}

        desc = inv["description"]
        desc_l = desc.lower()
        client_contact = (inv.get("client_contact") or "").strip()
        client_name = inv["client_name"]
        slug = f"p-{invoice_id.lower()}"

        if "resume" in desc_l or "cover letter" in desc_l:
            ptype = "ATS_RESUME"
            prompt = f"Client: {client_name}. Service: {desc}. Ek clean, modern, print-ready standalone HTML5 ATS Resume + Cover Letter page banao (dark/light clean professional CSS, Print to PDF button ke saath). Sirf pure HTML code do."
        elif "mini-website" in desc_l or "qr menu" in desc_l or "website" in desc_l:
            ptype = "MINI_WEBSITE"
            prompt = f"Client/Shop: {client_name}. Contact: {client_contact}. Details: {desc}. Ek sundar mobile-friendly standalone HTML5 Business Mini-Website + Menu/Services cards + WhatsApp Order button banao. Sirf pure HTML code do."
        else:
            ptype = "VIRTUAL_OFFICE"
            prompt = f"Company: {client_name}. Plan: {desc}. Ek clean Digital Virtual Office Onboarding Portal standalone HTML5 page banao (Task Checklist, Attendance Link, Team Guide ke saath). Sirf pure HTML code do."

        html_out = smart_generate(prompt, system_prompt="Return ONLY clean standalone HTML starting with <!DOCTYPE html>. No markdown fences.", model=PRIMARY_MODEL)
        html_out = html_out.strip().removeprefix("```html").removeprefix("```").removesuffix("```").strip()

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO client_pages (slug, client_name, page_type, html_content) VALUES (%s,%s,%s,%s) ON CONFLICT (slug) DO UPDATE SET html_content = EXCLUDED.html_content;",
                    (slug, client_name[:140], ptype, html_out)
                )

        live_url = f"{PUBLIC_URL}/p/{slug}"
        if "@" in client_contact:
            send_email_https(
                client_contact,
                f"Your {desc} is Ready! — aIValue8",
                f"Namaste {client_name},\n\nAapka order ({invoice_id}) ready aur LIVE ho gaya hai!\n\n👉 Open / Download Here: {live_url}\n\nDhanyawad,\naIValue8 Corporation"
            )

        send_alert(f"📦 AUTO-FULFILLED & LIVE!\nClient: {client_name}\nType: {ptype}\n🔗 Link: {live_url}")
        return {"status": "fulfilled", "live_url": live_url, "type": ptype}
    finally:
        conn.close()
