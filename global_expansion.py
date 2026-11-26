import os
import json
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

def generate_global_enterprise_proposal(client_name: str, country: str, industry: str, requirement: str) -> dict:
    """Generates a borderless, multi-currency high-ticket enterprise sovereign proposal for any country or industry."""
    prompt = f"""
    Global Client: {client_name}
    Country / Region: {country}
    Industry: {industry}
    Core Requirement: {requirement}
    
    Tum aIValue8 Sovereign Corporation ke Global Expansion & Enterprise Architect ho. Is international client ke liye ek multi-million dollar corporate level ka Technical Architecture & ROI Proposal (Value starting at $5,000 to $50,000 / Rs 4,00,000+) likho. Currency unke region ke hisab se (USD/EUR/AED/INR) mention karo.
    Reply ONLY valid JSON:
    {{
      "project_title": "Global Autonomous Enterprise Solution Title",
      "target_market": "{country} - {industry}",
      "estimated_value": "$10,000 USD (Approx ₹8,50,000 INR)",
      "global_compliance": "GDPR / DPDP / Cross-Border Secure",
      "executive_summary": "World-class architectural breakdown in professional English",
      "deliverables": ["Custom Multi-Lingual AI Cluster", "Global Secure Vault", "Real-time Autonomous Generative UI"]
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum Global Enterprise Solutions Architect ho.", model=PRIMARY_MODEL, json_mode=True)
    proposal = json.loads(raw)

    send_alert(
        f"🌍 GLOBAL ENTERPRISE PROPOSAL GENERATED!\n"
        f"🏢 Client: {client_name} ({country})\n"
        f"🏭 Industry: {industry}\n"
        f"📦 Project: {proposal.get('project_title')}\n"
        f"💰 Global Value: {proposal.get('estimated_value')}\n"
        f"🌐 Compliance: {proposal.get('global_compliance')}"
    )
    return {"status": "global_proposal_ready", "proposal": proposal}
