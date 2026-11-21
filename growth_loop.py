import json
import datetime
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

def run_performance_loop() -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get views today vs yesterday
            cur.execute("SELECT COUNT(*) as cnt FROM site_analytics WHERE created_at >= CURRENT_DATE;")
            views_today = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) as cnt FROM site_analytics WHERE created_at >= CURRENT_DATE - INTERVAL '1 day' AND created_at < CURRENT_DATE;")
            views_yesterday = cur.fetchone()["cnt"]

            # Get sales today vs yesterday
            cur.execute("SELECT COALESCE(SUM(amount_inr),0) as rev FROM invoices WHERE status='PAID' AND paid_at >= CURRENT_DATE;")
            rev_today = float(cur.fetchone()["rev"])
            cur.execute("SELECT COALESCE(SUM(amount_inr),0) as rev FROM invoices WHERE status='PAID' AND paid_at >= CURRENT_DATE - INTERVAL '1 day' AND paid_at < CURRENT_DATE;")
            rev_yesterday = float(cur.fetchone()["rev"])

        # Check for performance drop
        is_drop = (views_today < views_yesterday) or (rev_today < rev_yesterday)
        
        loop_status = "OPTIMAL & GROWING 🚀"
        corrective_plan = "All departments collaborating well. Continue multi-industry lead hunting and social sharing."

        if is_drop:
            loop_status = "PERFORMANCE DIP DETECTED — BD TASKFORCE ACTIVATED ⚠️"
            prompt = f"""
            Performance Data Comparison:
            - Views Yesterday: {views_yesterday} | Views Today: {views_today}
            - Revenue Yesterday: ₹{rev_yesterday} | Revenue Today: ₹{rev_today}
            
            Tum aIValue8 ki Cross-Functional Business Development & Strategy Team ho. 
            Koi bhi ego ya single-player approach nahi hai; COO, CFO, CSO aur Marketing milkar loop mein kaam kar rahe hain.
            Dip aane ke 2 sabse bade karan aur usko theek karne ka ek quick action plan (Hinglish mein) batao.
            Reply ONLY JSON: {{"root_cause":"1-line analysis","action_plan":"2-line team execution fix"}}
            """
            raw = smart_generate(prompt, system_prompt="Tum aIValue8 ke Chief Strategy Officer ho.", model=PRIMARY_MODEL, json_mode=True)
            analysis = json.loads(raw)
            corrective_plan = f"Reason: {analysis.get('root_cause')}\nFix: {analysis.get('action_plan')}"

        report_msg = (
            f"🔄 aIValue8 LOOP-CONNECTED PERFORMANCE REPORT:\n"
            f"📊 Status: {loop_status}\n"
            f"👀 Views (Today vs Yest): {views_today} vs {views_yesterday}\n"
            f"💰 Revenue (Today vs Yest): ₹{rev_today} vs ₹{rev_yesterday}\n\n"
            f"🤝 Cross-Team Coordination:\n{corrective_plan}"
        )
        send_alert(report_msg)
        return {"status": "loop_executed", "is_drop": is_drop, "views": {"today": views_today, "yest": views_yesterday}, "revenue": {"today": rev_today, "yest": rev_yesterday}, "plan": corrective_plan}
    finally:
        conn.close()
