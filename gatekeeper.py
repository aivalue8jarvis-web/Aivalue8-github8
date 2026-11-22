import json
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import smart_generate, PRIMARY_MODEL

def final_gatekeeper_review(output_type: str, raw_content: str, client_name: str) -> dict:
    """Final Gatekeeper: Checks end-to-end for zero mistakes, structural integrity, and saves a reusable modular clone vault template."""
    prompt = f"""
    Output Type: {output_type}
    Client: {client_name}
    Content to inspect: {raw_content[:2000]}
    
    Tum aIValue8 ke Final Gatekeeper ho. Check karo ki koi spelling, layout ya logical mistake na ho. 
    Saath hi ise ek 'Furnished Reusable Clone Template' mein convert karo taaki agar aage same requirement aaye toh seedha clone karke de sakein.
    Reply ONLY JSON:
    {{"approved": true, "audit_notes": "No errors found. Clean structure.", "clone_template_key": "template_slug_v1"}}
    """
    raw = smart_generate(prompt, system_prompt="Tum Final Gatekeeper ho.", model=PRIMARY_MODEL, json_mode=True)
    res = json.loads(raw)
    
    if res.get("approved"):
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO client_pages (slug, client_name, page_type, html_content) VALUES (%s,%s,%s,%s) ON CONFLICT (slug) DO UPDATE SET html_content = EXCLUDED.html_content;",
                        (res.get("clone_template_key", "vault_template"), client_name, output_type, raw_content)
                    )
        finally:
            conn.close()
    return res
