import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from mailer import send_email_https, extract_email
from matchmaker import dispatch_whatsapp_or_link

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def run_autonomous_sales_outreach() -> dict:
    """Pulls untargeted/new CRM leads and launches autonomous email/WhatsApp sales pitches."""
    conn = get_connection()
    outreach_results = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Fetch leads that haven't been pitched yet (outreach_stage = 0)
            cur.execute("SELECT * FROM crm_leads WHERE outreach_stage = 0 ORDER BY id DESC LIMIT 5;")
            leads = cur.fetchall()

        if not leads:
            return {"status": "no_pending_outreach", "sent_count": 0}

        for lead in leads:
            email = extract_email(lead["contact"]) or extract_email(lead["requirement"])
            name = lead["lead_name"]
            req = lead["requirement"]

            if email:
                # Generate AI Sales Pitch for Email
                prompt = f"""
                Target Lead: {name}
                Need/Requirement: {req}
                Our Solutions: ATS Resume (Rs 29), Local Shop Mini-Website (Rs 99), Virtual Office SaaS (Rs 49/mo), or Custom AI Automation.
                Write a short, professional, highly persuasive B2B sales email in Hinglish/English offering our solution with a direct link to {PUBLIC_URL}/store.
                Reply ONLY valid JSON: {{"subject": "Short catchy subject line", "body": "Clean 4-paragraph sales email body"}}
                """
                try:
                    raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Elite Sales Director ho.", model=PRIMARY_MODEL, json_mode=True)
                    mail_data = json.loads(raw)
                    
                    # Send via Brevo/HTTPS bridge
                    res = send_email_https(email, mail_data.get("subject", "Grow your business with aIValue8 AI"), mail_data.get("body", ""))
                    
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE crm_leads SET outreach_stage = 1, last_outreach_at = CURRENT_TIMESTAMP WHERE id = %s;", (lead["id"],))
                    
                    outreach_results.append({"target": email, "channel": "EMAIL", "status": "sent" if res.get("sent") else "logged_draft"})
                except Exception as ex:
                    print(f"Outreach email error for {email}: {ex}")
            else:
                # Fallback to WhatsApp / Phone outreach link
                pitch = f"Namaste {name}, aIValue8 Corporation se sampark hai. Aapki requirement ({req[:50]}) ke liye hum instant AI solutions provide karte hain. Visit: {PUBLIC_URL}/store"
                wa_res = dispatch_whatsapp_or_link(lead["contact"], pitch)
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE crm_leads SET outreach_stage = 1, last_outreach_at = CURRENT_TIMESTAMP WHERE id = %s;", (lead["id"],))
                outreach_results.append({"target": lead["contact"], "channel": "WHATSAPP_LINK", "status": "generated"})

        send_alert(f"🚀 AUTONOMOUS SALES OUTREACH RUN:\nProcessed {len(outreach_results)} new leads with tailored pitches.")
        return {"status": "outreach_executed", "sent_count": len(outreach_results), "details": outreach_results}
    finally:
        conn.close()
