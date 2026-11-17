import json
from database import get_connection
from sentinel import smart_generate, FALLBACK_MODEL

BLOCKED_KEYWORDS = [
    "gambling", "betting", "satta", "scam", "fraud", "otp bypass",
    "hack", "spam bulk", "fake review", "pirated", "crypto scam", "adult"
]

GOVERNANCE_PROMPT = """
Tum aIValue8 Corporation ke Chief Legal & Governance Officer (India) ho.
Har task, business idea, ya WhatsApp pitch ko in Indian laws ke hisaab se check karo:
1. DPDP Act 2023 (Personal data misuse/unauthorized scraping na ho)
2. IT Act & Cyber Laws (No fraud, phishing, fake identity)
3. RBI & Financial Compliance (No illegal chit funds, Ponzi, ya unauthorized lending)
4. ASCI Advertising & Anti-Spam Ethics (No misleading claims, no harassment)

Reply ONLY in valid JSON format:
{"approved": true/false, "reason": "short Hindi/Hinglish reason"}
"""

def check_compliance(action_type: str, payload: str) -> dict:
    text_lower = payload.lower()
    for word in BLOCKED_KEYWORDS:
        if word in text_lower:
            result = {"approved": False, "reason": f"Blocked keyword detected: '{word}' (Unethical/Illegal)"}
            _save_governance_log(action_type, payload, False, result["reason"])
            return result
    try:
        raw = smart_generate(
            f"Action Type: {action_type}\nContent/Idea: {payload}",
            system_prompt=GOVERNANCE_PROMPT,
            model=FALLBACK_MODEL,
            json_mode=True
        )
        result = json.loads(raw.strip())
        approved = bool(result.get("approved", False))
        reason = result.get("reason", "Checked")
    except Exception as e:
        approved = False
        reason = f"Governance safety hold (Error: {str(e)})"
    _save_governance_log(action_type, payload, approved, reason)
    return {"approved": approved, "reason": reason}

def _save_governance_log(action_type: str, payload: str, approved: bool, reason: str):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO governance_logs (action_type, payload, is_approved, reason) VALUES (%s, %s, %s, %s);",
                    (action_type, payload[:2000], approved, reason[:500])
                )
    finally:
        conn.close()
