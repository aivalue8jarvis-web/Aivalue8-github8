from sentinel import send_alert, diagnose_and_alert
from cloner import spawn_clone_agent
from hunter import run_opportunity_scan
from matchmaker import run_buyer_seller_matchmaker
from mailer import process_crm_outreach
from media_factory import generate_media_campaign

CORE_CLONES = [
    ("Research_Clone_01", "Research", "Tum Indian market aur B2B opportunities research karne wale AI agent ho."),
    ("Closer_Clone_01", "Sales", "Tum ethical Indian B2B Email aur WhatsApp deal closer agent ho."),
    ("Media_Clone_01", "Marketing", "Tum aIValue8 ke liye viral Hinglish Reels, YouTube scripts aur social posts banate ho.")
]

def run_daily_autopilot() -> dict:
    report = {"clones": [], "hunter": None, "matchmaker": None, "outreach": None, "media": None}

    for name, dept, role in CORE_CLONES:
        try:
            report["clones"].append(spawn_clone_agent(name, dept, role).get("status"))
        except Exception as e:
            diagnose_and_alert(f"autopilot.clone.{name}", e)

    for key, fn in [
        ("hunter", run_opportunity_scan),
        ("matchmaker", run_buyer_seller_matchmaker),
        ("outreach", process_crm_outreach),
        ("media", generate_media_campaign),
    ]:
        try:
            report[key] = fn()
        except Exception as e:
            diagnose_and_alert(f"autopilot.{key}", e)
            report[key] = {"error": str(e)}

    send_alert(
        f"🤖 aIValue8 DAILY CEO AUTO-PILOT REPORT:\n"
        f"🌍 New Opportunities: {(report['hunter'] or {}).get('new_saved', 0)}\n"
        f"🤝 New Trade Matches: {(report['matchmaker'] or {}).get('new_matches', 0)}\n"
        f"📧 Outreach Processed: {(report['outreach'] or {}).get('processed', 0)}\n"
        f"🎬 Media Campaign: {(report['media'] or {}).get('status', 'done')}"
    )
    return {"status": "autopilot_complete", "report": report}
