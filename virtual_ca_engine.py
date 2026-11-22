import os
import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from cloner import spawn_clone_agent
from payments import create_invoice

def init_virtual_ca_agent():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM agents_registry WHERE agent_name='Account_Head_CA_AI';")
            if not cur.fetchone():
                spawn_clone_agent(
                    "Account_Head_CA_AI",
                    "Finance_Tax",
                    "Tum aIValue8 ke Head Account CA AI ho. Small businesses ke financial documents (bills, GST, expenses) ko segregate karke clean tax ledger prepare karte ho aur compliance reminder dete ho."
                )
    finally:
        conn.close()

def process_client_financial_doc(client_name: str, client_contact: str, doc_description: str) -> dict:
    init_virtual_ca_agent()
    conn = get_connection()
    try:
        prompt = f"""
        Client: {client_name}
        Document/Expense Input: "{doc_description}"
        Tum Head CA AI ho. Is document ko analyze karo, category (Sales, Purchase, Rent, Utility, Taxes) mein segregate karo, aur annual Rs 999 subscription compliance status update do.
        Reply ONLY JSON:
        {{
          "category": "Expense Category",
          "tax_implication": "1-line tax observation",
          "ledger_entry": "Structured summary for ledger",
          "subscription_promo": "Remind them of the Rs 999/year unlimited annual compliance pass."
        }}
        """
        raw = smart_generate(prompt, system_prompt="Tum expert Virtual CA ho.", model=PRIMARY_MODEL, json_mode=True)
        analysis = json.loads(raw)

        send_alert(
            f"📊 VIRTUAL CA LEDGER ENTRY:\n"
            f"👤 Client: {client_name} ({client_contact})\n"
            f"📁 Category: {analysis.get('category')}\n"
            f"💡 Observation: {analysis.get('tax_implication')}\n"
            f"📝 Summary: {analysis.get('ledger_entry')}"
        )
        return {"status": "document_processed", "analysis": analysis}
    finally:
        conn.close()
