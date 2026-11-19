import os
import json
import datetime
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import send_alert
from mailer import send_email_https

BACKUP_EMAIL = os.getenv("BACKUP_EMAIL", "backup@sarahics.in").strip()
BACKUP_TABLES = ["treasury_wallets", "treasury_ledger", "crm_leads", "invoices", "agents_registry", "opportunities", "trade_matches"]

def run_daily_backup() -> dict:
    snapshot = {"exported_at": datetime.datetime.utcnow().isoformat() + "Z", "tables": {}}
    counts = {}
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for tbl in BACKUP_TABLES:
                cur.execute(f"SELECT * FROM {tbl};")
                rows = cur.fetchall()
                snapshot["tables"][tbl] = rows
                counts[tbl] = len(rows)
    finally:
        conn.close()

    json_dump = json.dumps(snapshot, default=str, ensure_ascii=False, indent=2)
    subject = f"aIValue8 Daily Backup ({datetime.date.today().isoformat()})"
    body = f"aIValue8 Corporation Daily Snapshot\nCounts: {json.dumps(counts)}\n\n--- JSON BACKUP ---\n{json_dump[:45000]}"

    email_res = send_email_https(BACKUP_EMAIL, subject, body)
    if email_res.get("sent"):
        send_alert(f"💾 DAILY BACKUP SENT to {BACKUP_EMAIL} ✅\nRecords: {counts}")
    else:
        send_alert(f"💾 BACKUP SNAPSHOT READY (Email pending — Brevo API key add karein):\n{counts}")
    return {"status": "backup_complete", "backup_email": BACKUP_EMAIL, "email_result": email_res, "counts": counts}
