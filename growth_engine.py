import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from cloner import spawn_clone_agent
from mailer import send_email_https

MARKETING_TEAM_CLONES = [
    ("Growth_Director_AI", "Marketing", "Tum aIValue8 ke Chief Growth & Traffic Officer ho. Duniya bhar se target viewers ko sarahics.in tak lane ke liye organic strategies banate ho."),
    ("SEO_Blogging_Bot", "Content", "Tum high-ranking search keywords par micro-articles aur landing page hooks likhte ho."),
    ("Social_Viral_Agent", "Social", "Tum Instagram aur YouTube Shorts ke liye high-conversion viral hooks aur video prompts design karte ho.")
]

def init_marketing_team():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for name, dept, role in MARKETING_TEAM_CLONES:
                cur.execute("SELECT 1 FROM agents_registry WHERE agent_name=%s;", (name,))
                if not cur.fetchone():
                    spawn_clone_agent(name, dept, role)
    finally:
      conn.close()

def run_growth_engine_task() -> dict:
    init_marketing_team()
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) as cnt FROM site_analytics;")
            total_views = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) as cnt FROM invoices WHERE status='PAID';")
            total_services = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) as cnt FROM crm_leads;")
            total_clients = cur.fetchone()["cnt"]

        prompt = f"""
        Current Real Metrics of aIValue8 (sarahics.in):
        - Total Visitors/Views: {total_views}
        - Total Services Delivered: {total_services}
        - Total Leads/Clients in CRM: {total_clients}

        Tum Growth Team ho. Aaj ka ek aisa action plan batao jisse bina ad budget ke organic traffic aur badhe aur visitors convert hon.
        Reply ONLY JSON: {{"campaign_focus":"1-line focus","action_item":"2-line execution step for Rayan","viral_hook":"1 catchy line for social media"}}
        """
        strat = json.loads(smart_generate(prompt, system_prompt="Tum Chief Growth Officer ho.", model=PRIMARY_MODEL, json_mode=True))
        send_alert(f"📈 aIValue8 GROWTH & TRAFFIC ENGINE REPORT:\n👀 Views: {total_views} | 📦 Services: {total_services} | 🤝 Clients: {total_clients}\n\n🎯 Focus: {strat.get('campaign_focus')}\n💡 Action: {strat.get('action_item')}\n🔥 Hook: {strat.get('viral_hook')}")
        return {"status": "growth_engine_ran", "metrics": {"views": total_views, "services": total_services, "clients": total_clients}, "strategy": strat}
    finally:
        conn.close()
