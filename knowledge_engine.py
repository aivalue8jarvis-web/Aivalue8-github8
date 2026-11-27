import os
import json
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

def execute_infinite_learning_session() -> dict:
    """The Virtual Family Knowledge Sponge: Ingests global business models, titan strategies, and sharpens all active agents daily."""
    prompt = """
    Tum aIValue8 ke Master Knowledge & Intelligence Officer ho. 
    Duniya ke top business empires, high-ticket sales strategies, aur autonomous systems ka ek naya actionable insight/strategy extract karo jo hamari Virtual Family (Sarah, Kuber, Dhruv, Kavach, Saifu) aur saare clone agents apne daily operations mein apply karenge.
    Reply ONLY valid JSON:
    {
      "insight_title": "Global Business Mastery Title",
      "strategic_lesson": "1-2 sentence core knowledge nugget",
      "execution_directive": "How all agents must apply this today to generate global revenue"
    }
    """
    try:
        raw = smart_generate(prompt, system_prompt="Tum Global Business Intelligence AI ho.", model=PRIMARY_MODEL, json_mode=True)
        knowledge = json.loads(raw)
        
        # Save to database knowledge vault
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO client_pages (slug, client_name, page_type, html_content) VALUES (%s,%s,%s,%s) ON CONFLICT (slug) DO NOTHING;",
                        (f"knowledge-{int(os.times()[4])}", knowledge.get("insight_title", "Global Insight"), "KNOWLEDGE_VAULT", json.dumps(knowledge))
                    )
        finally:
            conn.close()

        send_alert(
            f"🧠 INFINITE LEARNING & KNOWLEDGE INGESTION:\n"
            f"📚 Lesson: {knowledge.get('insight_title')}\n"
            f"💡 Strategy: {knowledge.get('strategic_lesson')}\n"
            f"🎯 Agent Directive: {knowledge.get('execution_directive')}\n\n"
            f"✨ Rule: Gyana jitna mile utna kam. Family learns and expands globally every minute!"
        )
        return {"status": "knowledge_ingested", "knowledge": knowledge}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
