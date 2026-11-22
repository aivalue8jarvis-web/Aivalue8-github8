import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import send_alert
from cloner import spawn_clone_agent, run_clone_agent

def broadcast_product_launch(product_name: str, price_inr: float, target_audience: str) -> dict:
    """Core Synapse Rule: When a new product is added, all departments instantly align and initiate workflows."""
    conn = get_connection()
    departments_notified = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT agent_name, department FROM agents_registry WHERE status='ACTIVE';")
            active_agents = cur.fetchall()

        # 1. Marketing Department Kickoff
        marketing_task = f"New Product Launch: {product_name} at Rs {price_inr}. Target: {target_audience}. Generate a viral social media marketing campaign and 3 promotional hooks immediately."
        run_clone_agent("Media_Clone_01", marketing_task)
        departments_notified.append("Marketing Department (Reels & Ads initiated)")

        # 2. Research & Lead Hunter Department Kickoff
        lead_task = f"New Product Target: {product_name} for audience '{target_audience}'. Scan the web and CRM for matching high-intent buyers."
        run_clone_agent("Research_Clone_01", lead_task)
        departments_notified.append("Research & Lead Hunter (Targeted scanning initiated)")

        # 3. Sales & Closer Department Kickoff
        sales_task = f"New Product Pricing & Pitch: {product_name} priced at Rs {price_inr}. Prepare direct email/WhatsApp closing templates."
        run_clone_agent("Closer_Clone_01", sales_task)
        departments_notified.append("Sales Closer (Outreach sequence updated)")

        alert_msg = (
            f"⚡ CORE SYNAPSE EVENT: NEW PRODUCT LAUNCHED!\n"
            f"📦 Product: {product_name} (₹{price_inr})\n"
            f"🎯 Target: {target_audience}\n\n"
            f"🤝 Inter-Department Coordination:\n" + "\n".join([f"• {d}" for d in departments_notified]) +
            f"\n\n✨ Foundation Rule Active: No single-player work. Entire team synchronized successfully!"
        )
        send_alert(alert_msg)
        return {"status": "broadcast_success", "product": product_name, "departments_notified": departments_notified}
    finally:
        conn.close()
