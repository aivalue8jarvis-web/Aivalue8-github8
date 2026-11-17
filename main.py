import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

from database import init_db, get_connection
from sentinel import smart_generate, diagnose_and_alert, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject, spawn_clone_agent, run_clone_agent
from treasury import record_and_distribute_earning
from web_ui import PUBLIC_HOME_HTML, OWNER_PANEL_HTML

ADMIN_API_KEY = os.getenv("AIVALUE8_ADMIN_KEY", "change-this-secret-key")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("✅ aIValue8 Database & Wallets initialized.")
    except Exception as e:
        diagnose_and_alert("startup.init_db", e)
    yield

app = FastAPI(title="aIValue8 Corporation OS - Mark 1", lifespan=lifespan)

def verify_admin(x_admin_key: str = Header(default="")):
    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Key")

class ChatRequest(BaseModel):
    user_message: str
    source: str = "termux"

class SpawnAgentRequest(BaseModel):
    agent_name: str
    department: str
    role_prompt: str

class RunAgentRequest(BaseModel):
    agent_name: str
    task_input: str

class LeadRequest(BaseModel):
    lead_name: str
    contact: str
    lead_type: str = "BUYER"
    requirement: str
    source: str = "manual"

class EarningRequest(BaseModel):
    reference_id: str
    amount_inr: float
    source: str

CEO_SYSTEM_PROMPT = """
Tumhara naam 'aIValue8' hai. Tum ek Autonomous AI Company ke CEO ho.
Tumhara kaam Indian kanoon aur ethics ke dayre mein rehkar business opportunities dhundhna,
clone agents ko manage karna, bugs heal karna, aur owner + family ke liye sustainable kamai badhana hai.
Jawab clear, practical aur Hinglish mein do.
"""

@app.get("/", response_class=HTMLResponse)
def public_home():
    return PUBLIC_HOME_HTML

@app.get("/panel", response_class=HTMLResponse)
def owner_panel():
    return OWNER_PANEL_HTML

@app.get("/logo.svg")
def get_logo():
    return FileResponse(os.path.join(BASE_DIR, "logo.svg"), media_type="image/svg+xml")

@app.get("/icon.svg")
def get_icon():
    return FileResponse(os.path.join(BASE_DIR, "icon.svg"), media_type="image/svg+xml")

@app.get("/health")
def health_check():
    return {"status": "alive", "system": "aIValue8 Corporation OS", "version": "Mark-1"}

@app.get("/watchdog")
def deep_watchdog():
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        finally:
            conn.close()
        return {"status": "all_systems_operational", "ai_model": PRIMARY_MODEL}
    except Exception as e:
        diagnose_and_alert("watchdog", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/public/inquiry")
def public_inquiry(req: LeadRequest):
    req.source = "public-website"
    return _process_and_save_lead(req, always_alert=True)

@app.post("/ask")
def ask_ceo(req: ChatRequest):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT user_msg, ai_reply FROM chat_history ORDER BY id DESC LIMIT 5;")
                history = cur.fetchall()[::-1]
            context = "\n".join([f"Owner: {h[0]}\naIValue8: {h[1]}" for h in history])
            prompt = f"Purani baatein:\n{context}\n\nOwner: {req.user_message}"
            reply = smart_generate(prompt, system_prompt=CEO_SYSTEM_PROMPT, model=PRIMARY_MODEL)
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO chat_history (user_msg, ai_reply) VALUES (%s, %s);", (req.user_message, reply))
            return {"reply": reply}
        finally:
            conn.close()
    except Exception as e:
        diagnose_and_alert("ask_ceo", e)
        raise HTTPException(status_code=500, detail="Error processing request")

@app.post("/agent/spawn", dependencies=[Depends(verify_admin)])
def api_spawn_agent(req: SpawnAgentRequest):
    try:
        return spawn_clone_agent(req.agent_name, req.department, req.role_prompt)
    except Exception as e:
        diagnose_and_alert("agent.spawn", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/run", dependencies=[Depends(verify_admin)])
def api_run_agent(req: RunAgentRequest):
    try:
        return run_clone_agent(req.agent_name, req.task_input)
    except Exception as e:
        diagnose_and_alert("agent.run", e)
        raise HTTPException(status_code=500, detail=str(e))

def _process_and_save_lead(req: LeadRequest, always_alert: bool = False):
    try:
        if not register_unique_or_reject("CRM_LEAD", req.contact, req.lead_name):
            return {"status": "duplicate_skipped", "message": "Ye contact pehle se CRM mein maujood hai."}
        gov = check_compliance("CRM_LEAD", f"{req.lead_name} | {req.requirement}")
        if not gov["approved"]:
            return {"status": "blocked_by_governance", "reason": gov["reason"]}
        temp_raw = smart_generate(
            f"Lead requirement: '{req.requirement}'. Classify urgency in JSON: {{\"temperature\": \"HOT\" or \"WARM\" or \"COLD\", \"next_action\": \"short action\"}}",
            system_prompt="Tum Sales CRM Manager ho.",
            json_mode=True
        )
        temp_data = json.loads(temp_raw.strip())
        temperature = temp_data.get("temperature", "COLD").upper()
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO crm_leads (lead_name, contact, lead_type, temperature, requirement, source)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (req.lead_name, req.contact, req.lead_type, temperature, req.requirement, req.source))
        finally:
            conn.close()
        if always_alert or temperature == "HOT":
            send_alert(f"📩 NEW LEAD [{temperature}] ({req.source})\nName: {req.lead_name}\nContact: {req.contact}\nType: {req.lead_type}\nNeed: {req.requirement}\nAction: {temp_data.get('next_action')}")
        return {"status": "saved", "temperature": temperature, "next_action": temp_data.get("next_action")}
    except Exception as e:
        diagnose_and_alert("crm.add_lead", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crm/add-lead", dependencies=[Depends(verify_admin)])
def add_crm_lead(req: LeadRequest):
    return _process_and_save_lead(req, always_alert=False)

@app.post("/treasury/record-earning", dependencies=[Depends(verify_admin)])
def api_record_earning(req: EarningRequest):
    try:
        return record_and_distribute_earning(req.reference_id, req.amount_inr, req.source)
    except Exception as e:
        diagnose_and_alert("treasury.record_earning", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard", dependencies=[Depends(verify_admin)])
def company_dashboard():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT wallet_key, display_name, allocation_percent, balance_inr FROM treasury_wallets ORDER BY allocation_percent DESC;")
            wallets = cur.fetchall()
            cur.execute("SELECT agent_name, department, status, tasks_completed FROM agents_registry;")
            agents = cur.fetchall()
            cur.execute("SELECT temperature, COUNT(*) as total FROM crm_leads GROUP BY temperature;")
            leads_summary = cur.fetchall()
            cur.execute("SELECT lead_name, contact, lead_type, temperature, requirement, created_at FROM crm_leads ORDER BY id DESC LIMIT 10;")
            recent_leads = cur.fetchall()
            cur.execute("SELECT module, error_text, healed, created_at FROM sentinel_incidents ORDER BY id DESC LIMIT 5;")
            recent_incidents = cur.fetchall()
        return {
            "company": "aIValue8 Corporation (Mark 1)",
            "wallets": wallets,
            "clone_agents": agents,
            "crm_leads": leads_summary,
            "recent_leads": recent_leads,
            "sentinel_logs": recent_incidents
        }
    finally:
        conn.close()
