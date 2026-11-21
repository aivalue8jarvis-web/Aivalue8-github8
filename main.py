import os
import json
import time
import base64
from typing import Optional
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Depends, Request, Body
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from google.genai import types

from database import init_db, get_connection
from sentinel import smart_generate, diagnose_and_alert, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject, spawn_clone_agent, run_clone_agent
from treasury import record_and_distribute_earning, verify_gateway_signature
from hunter import run_opportunity_scan, generate_daily_venture
from payments import create_invoice, get_invoice, submit_utr_proof, approve_and_settle_invoice, render_invoice_html
from matchmaker import run_buyer_seller_matchmaker, evaluate_lead_with_cfo
from mailer import process_crm_outreach, handle_email_reply
from media_factory import generate_media_campaign
from autopilot import run_daily_autopilot
from web_ui import PUBLIC_HOME_HTML, OWNER_PANEL_HTML

ADMIN_API_KEY = os.getenv("AIVALUE8_ADMIN_KEY", "change-this-secret-key")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
eval_rate_limit = defaultdict(list)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("✅ aIValue8 Mark-3.0 Database initialized.")
    except Exception as e:
        diagnose_and_alert("startup.init_db", e)
    yield

app = FastAPI(title="aIValue8 Corporation OS - Mark 3.0", lifespan=lifespan)

def verify_admin(x_admin_key: str = Header(default="")):
    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Key")

def check_rate(ip: str, limit: int = 6, window_sec: int = 900) -> bool:
    now = time.time()
    eval_rate_limit[ip] = [t for t in eval_rate_limit[ip] if now - t < window_sec]
    if len(eval_rate_limit[ip]) >= limit:
        return False
    eval_rate_limit[ip].append(now)
    return True

class ChatRequest(BaseModel):
    user_message: str
    source: str = "termux"

class EvaluateRequest(BaseModel):
    business_idea: str

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

class InvoiceRequest(BaseModel):
    client_name: str
    client_contact: str = ""
    description: str
    amount_inr: float

class UtrRequest(BaseModel):
    utr_number: str

class EmailReplyRequest(BaseModel):
    sender_email: str
    subject: str = "Inquiry"
    reply_text: str

class MediaRequest(BaseModel):
    topic: str = ""
    platform: str = "Instagram Reels & YouTube Shorts"

class VisionRequest(BaseModel):
    filename: str
    image_base64: str = ""
    mime_type: str = "image/png"
    note: str = ""

CEO_PROMPT = "Tumhara naam 'aIValue8' hai. Tum ek Autonomous Indian AI Company ke CEO ho. Indian rules aur ethics ke saath practical Hinglish mein jawab do."

@app.get("/", response_class=HTMLResponse)
def public_home():
    return PUBLIC_HOME_HTML

@app.get("/panel", response_class=HTMLResponse)
def owner_panel():
    return OWNER_PANEL_HTML

@app.get("/logo.svg")
def get_logo():
    p = os.path.join(BASE_DIR, "logo.svg")
    if not os.path.exists(p):
        raise HTTPException(status_code=404, detail="logo.svg not found")
    return FileResponse(p, media_type="image/svg+xml")

@app.get("/icon.svg")
def get_icon():
    p = os.path.join(BASE_DIR, "icon.svg")
    if not os.path.exists(p):
        raise HTTPException(status_code=404, detail="icon.svg not found")
    return FileResponse(p, media_type="image/svg+xml")

@app.get("/health")
def health_check():
    return {"status": "alive", "system": "aIValue8 Corporation OS", "version": "Mark-3.0"}

@app.get("/telegram/test", dependencies=[Depends(verify_admin)])
def test_telegram():
    import requests as rq
    tok = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        return {"ok": False, "token_set": bool(tok), "chat_id_set": bool(cid), "error": "Render Environment mein TELEGRAM_BOT_TOKEN ya TELEGRAM_CHAT_ID missing hai!"}
    r = rq.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": "✅ aIValue8 Telegram Alert Working!"}, timeout=10)
    return {"token_len": len(tok), "chat_id": cid, "telegram_response": r.json()}

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

@app.get("/public/telemetry")
def public_telemetry():
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM agents_registry WHERE status='ACTIVE';")
                ag = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM governance_logs WHERE is_approved=TRUE;")
                gv = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM sentinel_incidents WHERE healed=TRUE;")
                hl = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM opportunities;")
                op = cur.fetchone()[0]
        finally:
            conn.close()
        return {"active_agents": ag, "governance_checks": gv, "healed_bugs": hl, "opportunities_found": op}
    except Exception:
        return {"active_agents": 1, "governance_checks": 1, "healed_bugs": 1, "opportunities_found": 0}

@app.get("/public/showcase")
def public_showcase():
    try:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT title, platform, hook, script_body FROM media_campaigns ORDER BY id DESC LIMIT 3;")
                return {"campaigns": cur.fetchall()}
        finally:
            conn.close()
    except Exception:
        return {"campaigns": []}

@app.post("/public/evaluate")
def public_evaluate(req: EvaluateRequest, request: Request):
    idea = req.business_idea.strip()
    if len(idea) < 8:
        raise HTTPException(status_code=400, detail="Kam se kam 8 letters likhein.")
    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()
    if not check_rate(ip):
        raise HTTPException(status_code=429, detail="Thodi der baad try karein.")
    gov = check_compliance("PUBLIC_EVALUATOR", idea)
    if not gov["approved"]:
        raise HTTPException(status_code=400, detail=gov["reason"])
    try:
        prompt = f'Requirement: "{idea}". Evaluate strictly for AI, Growth, Web/App, Automation, CRM, or Trade Support. Reply ONLY JSON: {{"growth_score": 88, "category": "AI + Web & CRM", "summary": "2 line Hinglish insight", "steps": ["Step 1", "Step 2", "Step 3"], "launch_time": "7-14 Days"}}'
        return json.loads(smart_generate(prompt, system_prompt="Tum aIValue8 Evaluator ho.", json_mode=True))
    except Exception as e:
        diagnose_and_alert("public.evaluate", e)
        raise HTTPException(status_code=500, detail="AI busy hai, dubara try karein.")

@app.post("/public/inquiry")
def public_inquiry(req: LeadRequest):
    req.source = "public-website"
    return _save_lead(req, always_alert=True)

@app.post("/autopilot/run", dependencies=[Depends(verify_admin)])
def api_autopilot():
    return run_daily_autopilot()

@app.post("/hunter/scan", dependencies=[Depends(verify_admin)])
def api_hunter_scan():
    return run_opportunity_scan()

@app.post("/hunter/daily-venture", dependencies=[Depends(verify_admin)])
def api_daily_venture():
    return generate_daily_venture()

@app.post("/trade/match", dependencies=[Depends(verify_admin)])
def api_trade_match():
    return run_buyer_seller_matchmaker()

@app.post("/outreach/run", dependencies=[Depends(verify_admin)])
def api_outreach():
    return process_crm_outreach()

@app.post("/outreach/email-reply", dependencies=[Depends(verify_admin)])
def api_email_reply(req: EmailReplyRequest):
    return handle_email_reply(req.sender_email, req.subject, req.reply_text)

@app.post("/media/create", dependencies=[Depends(verify_admin)])
def api_media(req: Optional[MediaRequest] = Body(default=None)):
    topic = req.topic if req else ""
    plat = req.platform if req else "Instagram Reels & YouTube Shorts"
    return generate_media_campaign(topic, plat)

@app.post("/vision/evaluate", dependencies=[Depends(verify_admin)])
def api_vision_eval(req: VisionRequest):
    try:
        p_txt = f"Is screenshot/bill/product ({req.filename}) ko evaluate karo. Note: {req.note}. Reply ONLY JSON: {{\"eval_type\":\"BILL or ERROR or IDEA or PRODUCT\",\"summary\":\"2 line crisp Hinglish evaluation for voice\",\"estimated_value_inr\":0}}"
        contents = p_txt
        if req.image_base64:
            img_part = types.Part.from_bytes(data=base64.b64decode(req.image_base64), mime_type=req.mime_type)
            contents = [p_txt, img_part]
        res = json.loads(smart_generate(contents, system_prompt="Tum aIValue8 Vision Evaluator ho.", model="gemini-3.5-flash-lite", json_mode=True))
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO vision_evaluations (filename,eval_type,summary,estimated_value_inr) VALUES (%s,%s,%s,%s);", (req.filename[:190], res.get("eval_type", "SCREENSHOT")[:45], res.get("summary", ""), float(res.get("estimated_value_inr", 0))))
        finally:
            conn.close()
        send_alert(f"👁️ PHONE VISION [{res.get('eval_type')}]: {req.filename}\n{res.get('summary')}")
        return {"status": "evaluated", "evaluation": res}
    except Exception as e:
        diagnose_and_alert("vision.evaluate", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/invoices/create", dependencies=[Depends(verify_admin)])
def api_create_invoice(req: InvoiceRequest):
    return create_invoice(req.client_name, req.client_contact, req.description, req.amount_inr)

@app.get("/pay/{invoice_id}", response_class=HTMLResponse)
def view_invoice(invoice_id: str):
    inv = get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice nahi mili.")
    return render_invoice_html(inv)

@app.post("/pay/{invoice_id}/submit-utr")
def api_submit_utr(invoice_id: str, req: UtrRequest):
    try:
        return submit_utr_proof(invoice_id, req.utr_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/invoices/{invoice_id}/approve", dependencies=[Depends(verify_admin)])
def api_approve_invoice(invoice_id: str):
    return approve_and_settle_invoice(invoice_id)

@app.post("/webhooks/razorpay")
async def razorpay_webhook(request: Request, x_razorpay_signature: str = Header(default="")):
    body = await request.body()
    if not verify_gateway_signature(body, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    data = json.loads(body.decode("utf-8"))
    if data.get("event") == "payment.captured":
        ent = data["payload"]["payment"]["entity"]
        return record_and_distribute_earning(ent["id"], ent["amount"] / 100.0, "Razorpay Gateway")
    return {"status": "ignored"}

@app.post("/ask")
def ask_ceo(req: ChatRequest):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT user_msg, ai_reply FROM chat_history ORDER BY id DESC LIMIT 5;")
                hist = cur.fetchall()[::-1]
            ctx = "\n".join([f"Owner: {h[0]}\naIValue8: {h[1]}" for h in hist])
            reply = smart_generate(f"Purani baatein:\n{ctx}\n\nOwner: {req.user_message}", system_prompt=CEO_PROMPT, model=PRIMARY_MODEL)
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO chat_history (user_msg, ai_reply) VALUES (%s,%s);", (req.user_message, reply))
            return {"reply": reply}
        finally:
            conn.close()
    except Exception as e:
        diagnose_and_alert("ask_ceo", e)
        raise HTTPException(status_code=500, detail="Error")

@app.post("/agent/spawn", dependencies=[Depends(verify_admin)])
def api_spawn(req: SpawnAgentRequest):
    return spawn_clone_agent(req.agent_name, req.department, req.role_prompt)

@app.post("/agent/run", dependencies=[Depends(verify_admin)])
def api_run(req: RunAgentRequest):
    return run_clone_agent(req.agent_name, req.task_input)

def _save_lead(req: LeadRequest, always_alert: bool = False):
    try:
        if not register_unique_or_reject("CRM_LEAD", req.contact, req.lead_name):
            return {"status": "duplicate_skipped", "message": "Ye contact pehle se CRM mein hai."}
        gov = check_compliance("CRM_LEAD", f"{req.lead_name} | {req.requirement}")
        if not gov["approved"]:
            return {"status": "blocked_by_governance", "reason": gov["reason"]}
        t_data = json.loads(smart_generate(f"Requirement: '{req.requirement}'. Reply JSON: {{\"temperature\":\"HOT\" or \"WARM\" or \"COLD\",\"next_action\":\"short action\"}}", system_prompt="Sales CRM Manager", json_mode=True))
        temp = t_data.get("temperature", "COLD").upper()
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO crm_leads (lead_name,contact,lead_type,temperature,requirement,source) VALUES (%s,%s,%s,%s,%s,%s);", (req.lead_name, req.contact, req.lead_type, temp, req.requirement, req.source))
        finally:
            conn.close()
        if always_alert or temp == "HOT":
            send_alert(f"📩 NEW LEAD [{temp}] ({req.source})\nName: {req.lead_name}\nContact: {req.contact}\nNeed: {req.requirement}")
        return {"status": "saved", "temperature": temp, "next_action": t_data.get("next_action")}
    except Exception as e:
        diagnose_and_alert("crm.add_lead", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crm/add-lead", dependencies=[Depends(verify_admin)])
def add_crm_lead(req: LeadRequest):
    return _save_lead(req, always_alert=False)

@app.post("/treasury/record-earning", dependencies=[Depends(verify_admin)])
def api_earn(req: EarningRequest):
    return record_and_distribute_earning(req.reference_id, req.amount_inr, req.source)

@app.get("/dashboard", dependencies=[Depends(verify_admin)])
def company_dashboard():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT wallet_key, display_name, allocation_percent, balance_inr FROM treasury_wallets ORDER BY allocation_percent DESC;")
            wallets = cur.fetchall()
            cur.execute("SELECT agent_name, department, status, tasks_completed FROM agents_registry;")
            agents = cur.fetchall()
            cur.execute("SELECT lead_name, contact, lead_type, temperature, outreach_stage, requirement, created_at FROM crm_leads ORDER BY id DESC LIMIT 10;")
            leads = cur.fetchall()
            cur.execute("SELECT title, category, score, action_plan, created_at FROM opportunities ORDER BY id DESC LIMIT 10;")
            opps = cur.fetchall()
            cur.execute("SELECT invoice_id, client_name, amount_inr, status, utr_number, created_at FROM invoices ORDER BY created_at DESC LIMIT 10;")
            invs = cur.fetchall()
            cur.execute("SELECT buyer_name, seller_name, item_summary, match_score, whatsapp_pitch FROM trade_matches ORDER BY id DESC LIMIT 10;")
            matches = cur.fetchall()
            cur.execute("SELECT title, platform, hook, visual_prompt, created_at FROM media_campaigns ORDER BY id DESC LIMIT 6;")
            media = cur.fetchall()
            cur.execute("SELECT filename, eval_type, summary, estimated_value_inr, created_at FROM vision_evaluations ORDER BY id DESC LIMIT 6;")
            visions = cur.fetchall()
            cur.execute("SELECT module, error_text, healed, created_at FROM sentinel_incidents ORDER BY id DESC LIMIT 5;")
            logs = cur.fetchall()
        return {"company": "aIValue8 Corporation (Mark 3.0)", "wallets": wallets, "clone_agents": agents, "recent_leads": leads, "recent_opportunities": opps, "recent_invoices": invs, "trade_matches": matches, "media_campaigns": media, "vision_evals": visions, "sentinel_logs": logs}
    finally:
        conn.close()


from telegram_bot import handle_telegram_update, activate_telegram_webhook

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    return handle_telegram_update(data)

@app.get("/telegram/activate-webhook", dependencies=[Depends(verify_admin)])
def api_activate_tg():
    return activate_telegram_webhook()


from lead_hunter import hunt_public_leads
from backup import run_daily_backup

@app.post("/leads/hunt", dependencies=[Depends(verify_admin)])
def api_lead_hunt():
    return hunt_public_leads()

@app.post("/backup/run", dependencies=[Depends(verify_admin)])
def api_run_backup():
    return run_daily_backup()


@app.get("/media/{filename}")
def serve_reel_media(filename: str):
    safe = os.path.basename(filename)
    if not safe.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Invalid media file")
    path = os.path.join("/tmp/aivalue8_media", safe)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Media expired or not found")
    return FileResponse(path, media_type="video/mp4")


from autopilot import run_4x_industry_scan
from c_suite import run_csuite_board
from payments import reject_invoice

class RejectRequest(BaseModel):
    reason: str = "UTR mismatch"

@app.post("/scan/4x", dependencies=[Depends(verify_admin)])
def api_scan_4x():
    return run_4x_industry_scan()

@app.post("/csuite/run", dependencies=[Depends(verify_admin)])
def api_csuite():
    return run_csuite_board()

@app.post("/invoices/{invoice_id}/reject", dependencies=[Depends(verify_admin)])
def api_reject_invoice(invoice_id: str, req: RejectRequest):
    return reject_invoice(invoice_id, req.reason)


from social_publisher import debug_instagram_connection

@app.get("/instagram/debug", dependencies=[Depends(verify_admin)])
def api_ig_debug():
    return debug_instagram_connection()


@app.get("/store", response_class=HTMLResponse)
def public_store_page():
    return PUBLIC_HOME_HTML
