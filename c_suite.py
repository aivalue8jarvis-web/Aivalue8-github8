import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from cloner import spawn_clone_agent
from mailer import send_email_https

CEO_EMAIL = os.getenv("CEO_EMAIL", "ceo@sarahics.in").strip()
BACKUP_EMAIL = os.getenv("BACKUP_EMAIL", "backup@sarahics.in").strip()

MARKETING_EXEC_CLONES = [
    ("Marketing_Exec_01", "Marketing", "Tum Digital Virtual Office, Web/App aur AI services ke liye daily B2B clients aur startups dhundh kar polite outreach pitch banate ho."),
    ("VirtualOffice_Closer", "Sales", "Tum CA firms, field teams aur small businesses ko Digital Workplace SaaS (Rs 199/499/999 monthly plans) samjha kar demo book karte ho.")
]

def run_csuite_board() -> dict:
    conn = get_connection()
    results = {}
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT agent_name, department, tasks_completed FROM agents_registry WHERE status='ACTIVE';")
            agents = cur.fetchall()
            cur.execute("SELECT wallet_key, display_name, balance_inr FROM treasury_wallets;")
            wallets = cur.fetchall()
            cur.execute("SELECT status, COUNT(*) as cnt, COALESCE(SUM(amount_inr),0) as total FROM invoices GROUP BY status;")
            inv_stats = cur.fetchall()
            cur.execute("SELECT title, category, action_plan FROM opportunities ORDER BY id DESC LIMIT 3;")
            opps = cur.fetchall()
            cur.execute("SELECT lead_type, COUNT(*) as cnt FROM crm_leads GROUP BY lead_type;")
            lead_stats = cur.fetchall()

        coo_actions = []
        active_names = {a["agent_name"] for a in agents}
        for cname, dept, role in MARKETING_EXEC_CLONES:
            if cname not in active_names:
                sp = spawn_clone_agent(cname, dept, role)
                coo_actions.append(sp.get("status"))
            else:
                coo_actions.append(f"{cname}:active")
        results["COO"] = {"team": coo_actions, "active_agents": len(agents)}

        cfo_prompt = f"""
        Wallets: {json.dumps(wallets, default=str)}
        Invoices: {json.dumps(inv_stats, default=str)}
        Tum aIValue8 ke CFO & Virtual CA (vCA) ho (India).
        1) Minimum safe base pricing floor set karo (Website/App min Rs 3500, AI Automation min Rs 2500, Virtual Office Rs 199-999/mo) taaki zero-loss bargaining ho.
        2) GST/Tax reserve aur CA review checklist banao (note: final statutory UDIN sign insani CA karega).
        Reply ONLY JSON: {{"floor_rule":"2-line bargaining rule","vca_status":"2-line cashflow & tax audit note","ca_email_summary":"3-line clean report for human CA"}}
        """
        cfo_data = json.loads(smart_generate(cfo_prompt, system_prompt="Tum aIValue8 CFO & Virtual CA ho.", model=PRIMARY_MODEL, json_mode=True))
        results["CFO_vCA"] = cfo_data

        cso_prompt = f"""
        Latest Opportunities: {json.dumps(opps, default=str)}
        CRM Lead Types: {json.dumps(lead_stats, default=str)}
        Tum Chief Strategy Officer (CSO) ho. No-loss ethical capital-protected plan banao:
        Kaise hum Virtual Office, Web/App, AI Automation aur Job-Employer matching se aaj immediate revenue nikal sakte hain?
        Reply ONLY JSON: {{"priority_focus":"1-line focus","no_loss_rule":"1-line risk guard","today_action":"2-line execution move"}}
        """
        cso_data = json.loads(smart_generate(cso_prompt, system_prompt="Tum aIValue8 CSO ho.", model=PRIMARY_MODEL, json_mode=True))
        results["CSO"] = cso_data

        with conn:
            with conn.cursor() as cur:
                for off, data in [("COO", results["COO"]), ("CFO_vCA", cfo_data), ("CSO", cso_data)]:
                    cur.execute("INSERT INTO csuite_reports (officer, topic, plan_json) VALUES (%s,%s,%s);", (off, "Daily Executive Review", json.dumps(data)))

        send_email_https(CEO_EMAIL, "aIValue8 C-Suite Executive Brief", json.dumps(results, indent=2, ensure_ascii=False))
        send_email_https(BACKUP_EMAIL, "aIValue8 vCA Ledger Brief", cfo_data.get("ca_email_summary", ""))
        send_alert(
            f"🏛️ aIValue8 C-SUITE BOARD BRIEF:\n"
            f"👔 COO Team: {len(agents)} agents active\n"
            f"💹 CFO / vCA: {cfo_data.get('floor_rule')}\n"
            f"🧭 CSO Strategy: {cso_data.get('today_action')}\n"
            f"🛡️ Risk Guard: {cso_data.get('no_loss_rule')}"
        )
        return {"status": "csuite_complete", "board": results}
    finally:
        conn.close()
