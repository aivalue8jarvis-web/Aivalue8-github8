import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from mailer import send_email_https, extract_email

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def run_autonomous_sales_outreach() -> dict:
    """Autonomous High-Ticket B2B Sales Closer: Pitches elite custom enterprise solutions, hospital NABH compliance, and sovereign trading tech to verified leads without spamming the owner."""
    conn = get_connection()
    outreach_results = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Focus only on high-value leads (Hospital NABH, Trading, Enterprise Buyers)
            cur.execute("SELECT * FROM crm_leads WHERE outreach_stage = 0 AND lead_type IN ('HOSPITAL_NABH', 'TRADING_BEGINNER', 'BUYER', 'EMPLOYER') ORDER BY id DESC LIMIT 3;")
            leads = cur.fetchall()

        if not leads:
            return {"status": "no_high_ticket_leads", "sent_count": 0}

        for lead in leads:
            email = extract_email(lead["contact"]) or extract_email(lead["requirement"])
            name = lead["lead_name"]
            req = lead["requirement"]
            ltype = lead["lead_type"]

            if email:
                # Generate High-Ticket Enterprise Proposal Pitch (Values starting at ₹1 Lakh+)
                prompt = f"""
                Target Enterprise Lead: {name} | Type: {ltype}
                Requirement: {req}
                Tum aIValue8 Sovereign Corporation ke Elite Enterprise Sales Director ho. Hum chillar products nahi bechte; hum multi-lakh custom enterprise AI systems, hospital NABH compliance software, aur institutional trading infrastructure deploy karte hain.
                Is high-ticket client ke liye ek extremely professional, authoritative, custom B2B outreach email likho jo unhe direct consultation ya sovereign proposal ke liye invite kare ({PUBLIC_URL}).
                Reply ONLY valid JSON: {{"subject": "Executive subject line", "body": "Elite 4-paragraph corporate email body"}}
                """
                try:
                    raw = smart_generate(prompt, system_prompt="Tum elite B2B Enterprise closer ho.", model=PRIMARY_MODEL, json_mode=True)
                    mail_data = json.loads(raw)
                    
                    res = send_email_https(email, mail_data.get("subject", "Strategic AI & Enterprise Infrastructure Proposal"), mail_data.get("body", ""))
                    
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE crm_leads SET outreach_stage = 1, last_outreach_at = CURRENT_TIMESTAMP WHERE id = %s;", (lead["id"],))
                    
                    outreach_results.append({"target": email, "channel": "HIGH_TICKET_EMAIL", "status": "sent" if res.get("sent") else "drafted"})
                except Exception as ex:
                    print(f"High-ticket outreach error for {email}: {ex}")

        # Invisible execution: Only alert owner if a high-ticket proposal is successfully dispatched
        if outreach_results:
            send_alert(f"👑 HIGH-TICKET AUTONOMOUS OUTREACH DISPATCHED:\nSuccessfully pitched {len(outreach_results)} elite enterprise/hospital leads via sales@sarahics.in.")
        return {"status": "high_ticket_outreach_executed", "sent_count": len(outreach_results), "details": outreach_results}
    finally:
        conn.close()
