import hashlib
from database import get_connection
from sentinel import smart_generate, FALLBACK_MODEL
from governance import check_compliance

def compute_hash(text: str) -> str:
    normalized = " ".join(text.strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def register_unique_or_reject(entity_type: str, content: str, summary: str = "") -> bool:
    h = compute_hash(f"{entity_type}:{content}")
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dedup_registry WHERE content_hash = %s;", (h,))
                if cur.fetchone():
                    return False
                cur.execute(
                    "INSERT INTO dedup_registry (entity_type, content_hash, summary) VALUES (%s, %s, %s);",
                    (entity_type, h, summary[:300])
                )
                return True
    finally:
        conn.close()

def spawn_clone_agent(agent_name: str, department: str, role_prompt: str) -> dict:
    gov = check_compliance("SPAWN_AGENT", f"Dept: {department} | Role: {role_prompt}")
    if not gov["approved"]:
        return {"status": "rejected", "reason": gov["reason"]}
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO agents_registry (agent_name, department, role_prompt, model_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (agent_name) DO UPDATE
                    SET role_prompt = EXCLUDED.role_prompt, status = 'ACTIVE'
                    RETURNING id, agent_name, department, status;
                """, (agent_name, department, role_prompt, FALLBACK_MODEL))
                row = cur.fetchone()
                return {
                    "status": "spawned",
                    "agent_id": row[0],
                    "agent_name": row[1],
                    "department": row[2]
                }
    finally:
        conn.close()

def run_clone_agent(agent_name: str, task_input: str) -> dict:
    gov = check_compliance("AGENT_TASK", f"Agent: {agent_name} | Task: {task_input}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT role_prompt, model_id, status FROM agents_registry WHERE agent_name = %s;", (agent_name,))
            row = cur.fetchone()
            if not row or row[2] != "ACTIVE":
                return {"status": "error", "detail": f"Agent '{agent_name}' active nahi hai."}
            role_prompt, model_id, _ = row
        output = smart_generate(task_input, system_prompt=role_prompt, model=model_id)
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE agents_registry SET tasks_completed = tasks_completed + 1 WHERE agent_name = %s;", (agent_name,))
        return {"status": "success", "agent": agent_name, "output": output}
    finally:
        conn.close()
