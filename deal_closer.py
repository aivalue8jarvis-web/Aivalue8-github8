import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from payments import create_invoice
from fulfillment import fulfill_paid_order

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def run_autonomous_deal_negotiation() -> dict:
    """Scans pending CRM leads who replied or are warm, negotiates terms via AI, and auto-issues payment links."""
    conn = get_connection()
    closed_deals = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Look for warm or hot leads that need closing push
            cur.execute("SELECT * FROM crm_leads WHERE temperature IN ('HOT', 'WARM') AND outreach_stage BETWEEN 1 AND 3 LIMIT 3;")
            leads = cur.fetchall()

        for lead in leads:
            prompt = f"""
            Client Name: {lead['lead_name']}
            Requirement: {lead['requirement']}
            Lead Temperature: {lead['temperature']}
            Tum aIValue8 ke Master Autonomous Deal Closer ho. Is client ko closing ki taraf le jaane ke liye ek irresistible Hinglish/English offer aur closing pitch tayaar karo. Agar deal final lagti hai toh estimated price (e.g. 29 for resume, 99 for mini-site, 3500 for custom build) tay karo.
            Reply ONLY valid JSON:
            {{"ready_to_close": true, "amount_inr": 99, "service_desc": "Local Shop Mini-Website", "closing_pitch": "Polite persuasive closing message"}}
            """
            raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Top Sales Closer ho.", model=PRIMARY_MODEL, json_mode=True)
            deal_data = json.loads(raw)

            if deal_data.get("ready_to_close") and float(deal_data.get("amount_inr", 0)) > 0:
                amt = float(deal_data["amount_inr"])
                desc = deal_data.get("service_desc", "aIValue8 Digital Service")
                
                # Create invoice automatically
                inv = create_invoice(lead["lead_name"], lead["contact"], desc, amt)
                if inv.get("pay_path"):
                    pay_link = f"{PUBLIC_URL}{inv['pay_path']}"
                    pitch = f"{deal_data.get('closing_pitch')}\n\n💳 Secure UPI Checkout Link: {pay_link}"
                    
                    send_alert(
                        f"🤝 AUTONOMOUS DEAL PITCH CREATED!\n"
                        f"Client: {lead['lead_name']} ({lead['contact']})\n"
                        f"Service: {desc} (₹{amt})\n"
                        f"🔗 Link: {pay_link}\n\n"
                        f"💬 Pitch:\n{pitch}"
                    )
                    closed_deals.append({"client": lead["lead_name"], "invoice": inv["invoice_id"], "amount": amt})

        return {"status": "deal_negotiation_complete", "proposals_sent": len(closed_deals), "deals": closed_deals}
    finally:
        conn.close()
