import os
import json
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def generate_enterprise_sovereign_proposal(client_name: str, enterprise_need: str) -> dict:
    """Generates a high-ticket, no-bargain enterprise architectural proposal for elite clients."""
    prompt = f"""
    Enterprise Client: {client_name}
    Requirement / Industry Need: {enterprise_need}
    
    Tum aIValue8 Sovereign Corporation ke Chief Solutions Architect ho. Is high-ticket enterprise client ke liye ek heavy, elite, professional Technical Architecture & ROI Proposal (Value starting at Rs 1,00,000+) likho. Yeh aisa solution hona chahiye jise dekh kar client bina bargain kiye deal lock kare.
    Reply ONLY valid JSON:
    {{
      "project_title": "Enterprise Autonomous System Title",
      "estimated_value_inr": 150000,
      "roi_timeline": "30 Days deployment",
      "executive_summary": "High-impact architectural breakdown in professional English",
      "deliverables": ["Custom AI Agent Cluster", "Secure Private Vault", "Real-time Generative UI Dashboard"]
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum elite Enterprise Solutions Architect ho.", model=PRIMARY_MODEL, json_mode=True)
    proposal = json.loads(raw)
    
    gov = check_compliance("SOVEREIGN_PROPOSAL", f"{proposal.get('project_title')} | {proposal.get('executive_summary')}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}

    send_alert(
        f"👑 HIGH-TICKET SOVEREIGN PROPOSAL GENERATED!\n"
        f"🏢 Client: {client_name}\n"
        f"📦 Project: {proposal.get('project_title')}\n"
        f"💰 Ticket Value: ₹{proposal.get('estimated_value_inr'):,}\n"
        f"⏱️ Timeline: {proposal.get('roi_timeline')}\n"
        f"💡 Summary: {proposal.get('executive_summary')[:200]}"
    )
    return {"status": "proposal_ready", "proposal": proposal}
