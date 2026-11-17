import os
import psycopg2

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise ValueError("NEON_DATABASE_URL missing!")
    return psycopg2.connect(DATABASE_URL)

TABLES = [
    "CREATE TABLE IF NOT EXISTS chat_history (id SERIAL PRIMARY KEY, user_msg TEXT NOT NULL, ai_reply TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS agents_registry (id SERIAL PRIMARY KEY, agent_name VARCHAR(100) UNIQUE NOT NULL, department VARCHAR(50) NOT NULL, role_prompt TEXT NOT NULL, model_id VARCHAR(50) DEFAULT 'gemini-3.5-flash-lite', status VARCHAR(20) DEFAULT 'ACTIVE', tasks_completed INT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS dedup_registry (id SERIAL PRIMARY KEY, entity_type VARCHAR(50) NOT NULL, content_hash VARCHAR(64) UNIQUE NOT NULL, summary TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS governance_logs (id SERIAL PRIMARY KEY, action_type VARCHAR(50), payload TEXT, is_approved BOOLEAN, reason TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS crm_leads (id SERIAL PRIMARY KEY, lead_name VARCHAR(150), contact VARCHAR(100) UNIQUE NOT NULL, lead_type VARCHAR(30) DEFAULT 'BUYER', temperature VARCHAR(20) DEFAULT 'COLD', requirement TEXT, source VARCHAR(50), outreach_stage INT DEFAULT 0, last_outreach_at TIMESTAMP, last_followup TIMESTAMP DEFAULT CURRENT_TIMESTAMP, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "ALTER TABLE crm_leads ADD COLUMN IF NOT EXISTS outreach_stage INT DEFAULT 0;",
    "ALTER TABLE crm_leads ADD COLUMN IF NOT EXISTS last_outreach_at TIMESTAMP;",
    "CREATE TABLE IF NOT EXISTS treasury_wallets (wallet_key VARCHAR(50) PRIMARY KEY, display_name VARCHAR(100) NOT NULL, allocation_percent NUMERIC(5,2) NOT NULL, balance_inr NUMERIC(12,2) DEFAULT 0.00, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS treasury_ledger (id SERIAL PRIMARY KEY, reference_id VARCHAR(100) UNIQUE NOT NULL, gross_amount_inr NUMERIC(12,2) NOT NULL, source VARCHAR(100), split_details JSONB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS sentinel_incidents (id SERIAL PRIMARY KEY, module VARCHAR(50), error_text TEXT, ai_diagnosis TEXT, healed BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS opportunities (id SERIAL PRIMARY KEY, title VARCHAR(250) NOT NULL, category VARCHAR(60), score INT DEFAULT 80, action_plan TEXT, source VARCHAR(100), status VARCHAR(30) DEFAULT 'NEW', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS invoices (invoice_id VARCHAR(40) PRIMARY KEY, client_name VARCHAR(150) NOT NULL, client_contact VARCHAR(100), description TEXT NOT NULL, amount_inr NUMERIC(12,2) NOT NULL, payment_mode VARCHAR(30) DEFAULT 'DIRECT_BANK', utr_number VARCHAR(100), status VARCHAR(30) DEFAULT 'PENDING', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, paid_at TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS trade_matches (id SERIAL PRIMARY KEY, buyer_name VARCHAR(150), seller_name VARCHAR(150), item_summary TEXT, match_score INT DEFAULT 80, whatsapp_pitch TEXT, status VARCHAR(30) DEFAULT 'MATCHED', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS media_campaigns (id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL, platform VARCHAR(50), hook TEXT, script_body TEXT, caption TEXT, visual_prompt TEXT, status VARCHAR(30) DEFAULT 'READY', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    "CREATE TABLE IF NOT EXISTS vision_evaluations (id SERIAL PRIMARY KEY, filename VARCHAR(200), eval_type VARCHAR(50), summary TEXT, estimated_value_inr NUMERIC(12,2) DEFAULT 0.00, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
]

WALLETS = [
    ("survival_api", "Server, Domain & AI Survival Fund", 20.00),
    ("upgrade_reserve", "System Self-Upgrade Fund", 15.00),
    ("tax_gst", "Indian Tax & Compliance Reserve", 15.00),
    ("kids_pocket_box", "Bachhon ka Pocket Money Box", 10.00),
    ("owner_salary", "Owner Salary Wallet", 40.00),
]

def init_db():
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                for sql in TABLES:
                    cur.execute(sql)
                for k, n, p in WALLETS:
                    cur.execute("INSERT INTO treasury_wallets (wallet_key, display_name, allocation_percent) VALUES (%s,%s,%s) ON CONFLICT (wallet_key) DO NOTHING;", (k, n, p))
    finally:
        conn.close()
