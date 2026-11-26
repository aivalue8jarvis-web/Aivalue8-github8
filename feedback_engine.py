import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, PRIMARY_MODEL

def capture_and_learn_feedback(source_type: str, raw_input: str) -> str:
    """Auto-catches any minor feedback, client response, or instruction and embeds it into system intelligence."""
    if not raw_input or len(raw_input.strip()) < 3:
        return "Input too short to learn."
    
    prompt = f"""
    Source: {source_type}
    Raw User/Client Feedback or Input: "{raw_input}"
    Tum aIValue8 ke Self-Learning Core ho. Is input se ek choti, actionable business learning ya rule extract karo jisse future operations improve hon.
    Reply ONLY 1-2 crisp sentences of actionable learning in Hinglish/English.
    """
    try:
        learning = smart_generate(prompt, system_prompt="Tum self-learning AI optimizer ho.", model=PRIMARY_MODEL).strip()
    except Exception:
        learning = f"Processed input from {source_type}: {raw_input[:100]}"

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO feedback_memory (source_type, raw_input, ai_learning) VALUES (%s, %s, %s);",
                    (source_type[:45], raw_input[:2000], learning[:1000])
                )
    finally:
        conn.close()
    return learning
