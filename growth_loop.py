import json
import datetime
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

def get_analytics_metrics() -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Views Today vs Yesterday
            cur.execute("SELECT COUNT(*) as cnt FROM site_analytics WHERE created_at >= CURRENT_DATE;")
            v_today = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) as cnt FROM site_analytics WHERE created_at >= CURRENT_DATE - INTERVAL '1 day' AND created_at < CURRENT_DATE;")
            v_yest = cur.fetchone()["cnt"]

            # Services Delivered Today vs Yesterday
            cur.execute("SELECT COUNT(*) as cnt FROM invoices WHERE status='PAID' AND paid_at >= CURRENT_DATE;")
            s_today = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) as cnt FROM invoices WHERE status='PAID' AND paid_at >= CURRENT_DATE - INTERVAL '1 day' AND paid_at < CURRENT_DATE;")
            s_yest = cur.fetchone()["cnt"]

            # Total Happy Clients
            cur.execute("SELECT COUNT(*) as cnt FROM crm_leads;")
            total_clients = cur.fetchone()["cnt"]
    finally:
        conn.close()

    return {
        "views_today": v_today,
        "views_yesterday": v_yest,
        "services_today": s_today,
        "services_yesterday": s_yest,
        "total_clients": total_clients
    }

def run_performance_loop() -> dict:
    m = get_analytics_metrics()
    v_today, v_yest = m["views_today"], m["views_yesterday"]
    s_today, s_yest = m["services_today"], m["services_yesterday"]

    is_flat_or_down = (v_today < v_yest) or (s_today < s_yest)
    loop_status = "EXPONENTIAL MOMENTUM 🚀"
    corrective_plan = "All systems firing cylinders. Growth metrics are trending upwards smoothly."

    if is_flat_or_down:
        loop_status = "MOMENTUM BOOST ACTIVATED ⚡ (Targeting 2x Growth)"
        prompt = f"""
        Open-Source Analytics Comparison:
        - Views Yesterday: {v_yest} | Views Today: {v_today}
        - Services Yesterday: {s_yest} | Services Today: {s_today}
        
        Growth momentum thodi slow ya flat hui hai. aIValue8 ki non-egoistic team milkar ek instant micro-growth hack (jaise naya micro-service drop karna ya organic outreach) plan karegi.
        Reply ONLY JSON: {{"growth_tactic":"1-line aggressive strategy","team_action":"2-line execution step"}}
        """
        raw = smart_generate(prompt, system_prompt="Tum aIValue8 Chief Growth Officer ho.", model=PRIMARY_MODEL, json_mode=True)
        analysis = json.loads(raw)
        corrective_plan = f"Tactic: {analysis.get('growth_tactic')}\nAction: {analysis.get('team_action')}"

    report_msg = (
        f"📊 aIValue8 OPEN-SOURCE MOMENTUM REPORT:\n"
        f"⚡ Status: {loop_status}\n"
        f"👀 Views (Today vs Yest): {v_today} vs {v_yest}\n"
        f"📦 Services (Today vs Yest): {s_today} vs {s_yest}\n\n"
        f"🤝 Growth Team Action:\n{corrective_plan}"
    )
    send_alert(report_msg)
    return {"status": "momentum_loop_executed", "metrics": m, "plan": corrective_plan}
