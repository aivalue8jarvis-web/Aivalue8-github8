import re
from database import get_connection
from sentinel import send_alert, diagnose_and_alert
from cloner import spawn_clone_agent, run_clone_agent
from lead_hunter import hunt_public_leads
from hunter import run_opportunity_scan
from matchmaker import run_buyer_seller_matchmaker
from mailer import process_crm_outreach
from media_factory import generate_media_campaign
from backup import run_daily_backup

CORE_CLONES = [
    ("Research_Clone_01", "Research", "Tum Indian market aur B2B opportunities research karne wale AI agent ho."),
    ("Closer_Clone_01", "Sales", "Tum ethical Indian B2B Email aur WhatsApp deal closer agent ho."),
    ("Media_Clone_01", "Marketing", "Tum aIValue8 ke liye viral Hinglish Reels, YouTube scripts aur social posts banate ho.")
]

def run_daily_autopilot() -> dict:
    report = {"clones": [], "dynamic_clones": [], "lead_hunt": None, "hunter": None, "matchmaker": None, "outreach": None, "media": None, "backup": None}

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for name, dept, role in CORE_CLONES:
                cur.execute("SELECT 1 FROM agents_registry WHERE agent_name=%s;", (name,))
                if cur.fetchone():
                    report["clones"].append("active")
                else:
                    report["clones"].append(spawn_clone_agent(name, dept, role).get("status"))
    except Exception as e:
        diagnose_and_alert("autopilot.clones", e)
    finally:
        conn.close()

    for key, fn in [
        ("lead_hunt", hunt_public_leads),
        ("hunter", run_opportunity_scan),
        ("matchmaker", run_buyer_seller_matchmaker),
        ("outreach", process_crm_outreach),
        ("media", generate_media_campaign),
        ("backup", run_daily_backup),
    ]:
        try:
            report[key] = fn()
        except Exception as e:
            diagnose_and_alert(f"autopilot.{key}", e)
            report[key] = {"error": str(e)}

    # Dynamic Niche Clone Spawner: Har nayi opportunity par khud ek naya Clone Agent banaye!
    for opp in (report.get("hunter") or {}).get("opportunities", [])[:1]:
        try:
            title = opp.get("title", "Growth")
            slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")[:18] or "Niche"
            cname = f"Clone_{slug}"
            sp = spawn_clone_agent(cname, opp.get("category", "Growth"), f"Tum '{title}' niche mein clients dhundhne aur deal pitch karne wale specialized agent ho.")
            if sp.get("status") == "spawned":
                run_clone_agent(cname, f"Is opportunity par pehla 3-step client acquisition plan aur 1 short outreach message banao: {title} — {opp.get('action_plan')}")
                report["dynamic_clones"].append(cname)
        except Exception as e:
            diagnose_and_alert("autopilot.dynamic_clone", e)

    send_alert(
        f"🤖 aIValue8 DAILY CEO AUTO-PILOT REPORT:\n"
        f"🕵️‍♂️ New Leads Found: {(report['lead_hunt'] or {}).get('new_leads', 0)}\n"
        f"🌍 New Opportunities: {(report['hunter'] or {}).get('new_saved', 0)}\n"
        f"🧬 New Clones Created: {len(report['dynamic_clones'])}\n"
        f"🤝 New Trade Matches: {(report['matchmaker'] or {}).get('new_matches', 0)}\n"
        f"📧 Outreach Processed: {(report['outreach'] or {}).get('processed', 0)}\n"
        f"🎬 Media Campaign: {(report['media'] or {}).get('status', 'done')}\n"
        f"💾 Backup: {(report['backup'] or {}).get('status', 'done')}"
    )
    return {"status": "autopilot_complete", "report": report}
