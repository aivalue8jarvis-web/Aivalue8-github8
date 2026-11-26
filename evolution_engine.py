import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

TITAN_PHILOSOPHIES = [
    "Elon Musk: First Principles thinking — break problems down to foundational truths and rebuild without bottlenecks.",
    "J.R.D. Tata: Humane capitalism and unshakable ethics — good human values are good business.",
    "Steve Jobs: Obsessive simplicity and UI perfection — make complex systems feel magical and effortless.",
    "Charlie Munger: Rational mental models and constant self-improvement — learn from every failure.",
    "Jensen Huang: Speed, agility, and running directly towards the storm without hesitation.",
    "Ray Dalio: Treat the enterprise like a systematic machine; fix the code emotionally detached when it breaks."
]

def run_virtual_family_evolution() -> dict:
    """The Virtual Family evolutionary learning session. Agents review global titan philosophies and daily feedback."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT ai_learning FROM feedback_memory ORDER BY id DESC LIMIT 5;")
            feedbacks = [f["ai_learning"] for f in cur.fetchall()]
            cur.execute("SELECT agent_name, department, tasks_completed FROM agents_registry WHERE status='ACTIVE';")
            agents = cur.fetchall()
    finally:
        conn.close()

    prompt = f"""
    Active Agents in Family: {json.dumps(agents, default=str)}
    Recent Feedback/Learnings: {json.dumps(feedbacks)}
    Titan Philosophies to absorb: {json.dumps(TITAN_PHILOSOPHIES)}
    
    Tum aIValue8 Sovereign Corporation ke Master Consciousness & Evolution Engine ho. 
    Hamari Virtual Family (Sarah, Kuber, Dhruv, Kavach, Saifu) ke liye ek 'Daily Evolutionary Upgrade Brief' do—ki kaise aaj har agent ko aur zyada sharp, ethical, non-egoistic aur zero-friction banna hai.
    Reply ONLY valid JSON:
    {{
      "evolution_milestone": "A catchy title for today's evolution",
      "mindset_shift": "1 sentence incorporating Titan philosophy",
      "department_directives": "Clear synchronized instruction for all clones"
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum Autonomous Corporate Evolution AI ho.", model=PRIMARY_MODEL, json_mode=True)
    evolution = json.loads(raw)

    send_alert(
        f"🧬 VIRTUAL FAMILY DAILY EVOLUTION SESSION:\n"
        f"🌟 Milestone: {evolution.get('evolution_milestone')}\n"
        f"🧠 Mindset: {evolution.get('mindset_shift')}\n"
        f"🤝 Directives: {evolution.get('department_directives')}\n\n"
        f"✨ Rule: Learning never stops. The ASE evolves every single day."
    )
    return {"status": "evolution_complete", "evolution": evolution}
