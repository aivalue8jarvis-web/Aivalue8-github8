import os
import hmac
import hashlib
import json
from decimal import Decimal, ROUND_DOWN
from psycopg2.extras import RealDictCursor
from database import get_connection
from sentinel import send_alert

PAYMENT_WEBHOOK_SECRET = os.getenv("PAYMENT_WEBHOOK_SECRET", "")
UPGRADE_THRESHOLD_INR = Decimal("2000.00")

def verify_gateway_signature(payload_body: bytes, received_signature: str) -> bool:
    if not PAYMENT_WEBHOOK_SECRET:
        return False
    expected = hmac.new(
        PAYMENT_WEBHOOK_SECRET.encode("utf-8"),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, received_signature)

def record_and_distribute_earning(reference_id: str, amount_inr: float, source: str) -> dict:
    gross = Decimal(str(amount_inr)).quantize(Decimal("0.01"))
    if gross <= 0:
        raise ValueError("Amount 0 se zyada hona chahiye.")
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id FROM treasury_ledger WHERE reference_id = %s;", (reference_id,))
                if cur.fetchone():
                    return {"status": "duplicate_ignored", "reference_id": reference_id}
                cur.execute("SELECT wallet_key, display_name, allocation_percent, balance_inr FROM treasury_wallets;")
                wallets = cur.fetchall()
                split_details = {}
                allocated_total = Decimal("0.00")
                for w in wallets:
                    pct = Decimal(str(w["allocation_percent"]))
                    share = (gross * pct / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
                    split_details[w["wallet_key"]] = float(share)
                    allocated_total += share
                remainder = gross - allocated_total
                if "owner_salary" in split_details:
                    split_details["owner_salary"] = float(Decimal(str(split_details["owner_salary"])) + remainder)
                upgrade_balance = Decimal("0.00")
                for w in wallets:
                    key = w["wallet_key"]
                    add_amt = Decimal(str(split_details[key]))
                    new_bal = Decimal(str(w["balance_inr"])) + add_amt
                    if key == "upgrade_reserve":
                        upgrade_balance = new_bal
                    cur.execute(
                        "UPDATE treasury_wallets SET balance_inr = %s, updated_at = CURRENT_TIMESTAMP WHERE wallet_key = %s;",
                        (new_bal, key)
                    )
                cur.execute(
                    "INSERT INTO treasury_ledger (reference_id, gross_amount_inr, source, split_details) VALUES (%s, %s, %s, %s);",
                    (reference_id, gross, source, json.dumps(split_details))
                )
        if upgrade_balance >= UPGRADE_THRESHOLD_INR:
            send_alert(
                f"🚀 aIValue8 UPGRADE REMINDER!\n"
                f"Nayi kamai: ₹{gross} ({source})\n"
                f"Upgrade Reserve ab ₹{upgrade_balance} ho gaya hai! "
                f"Aap ab Cloud VPS / Video API upgrade approve kar sakte hain."
            )
        else:
            send_alert(
                f"💰 aIValue8 Earning Received: ₹{gross} ({source})\n"
                f"Owner Salary +₹{split_details.get('owner_salary')} | Kids Box +₹{split_details.get('kids_pocket_box')}"
            )
        return {"status": "distributed", "gross_inr": float(gross), "split": split_details}
    finally:
        conn.close()
