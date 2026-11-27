import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL

def handle_client_support_ticket(client_name: str, client_contact: str, query: str) -> dict:
    """Autonomous Support Agent: Handles customer inquiries, ticket routing, and instant automated resolution."""
    prompt = f"""
    Client Name: {client_name}
    Contact: {client_contact}
    Query/Issue: "{query}"
    
    Tum aIValue8 Corporation ke Head Client Success & Support Director ho. Is client query ka ek professional, reassuring, aur accurate solution Hinglish/English mein do. Agar order status ya resume delivery se juda hai toh /store ya workspace par guide karo.
    Reply ONLY valid JSON:
    {{
      "ticket_status": "RESOLVED or ESCALATED",
      "auto_reply": "Professional helpful support reply for the client",
      "escalate_to_owner": false
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum expert Client Support AI ho.", model=PRIMARY_MODEL, json_mode=True)
    ticket = json.loads(raw)

    if ticket.get("escalate_to_owner"):
        send_alert(
            f"⚠️ SUPPORT TICKET ESCALATED:\n"
            f"👤 Client: {client_name} ({client_contact})\n"
            f"❓ Query: {query}\n"
            f"🤖 AI Response: {ticket.get('auto_reply')}"
        )

    return {"status": "ticket_processed", "ticket": ticket}
