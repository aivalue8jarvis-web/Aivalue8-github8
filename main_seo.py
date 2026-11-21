# Dynamic micro-landing page generator for organic Google SEO traffic
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from database import get_connection
from psycopg2.extras import RealDictCursor

SEO_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — aIValue8 Autonomous AI OS</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    body{{background:#030712;color:#e2e8f0;font-family:sans-serif;padding:20px;line-height:1.6;}}
    .wrap{{max-width:700px;margin:40px auto;background:#0f172a;border:1px solid #1e293b;border-radius:18px;padding:30px;}}
    h1{{color:#38bdf8;font-size:28px;margin-bottom:15px;}}
    p{{color:#94a3b8;margin-bottom:20px;font-size:15px;}}
    .btn{{display:inline-block;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:bold;}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{title}</h1>
    <p>{description}</p>
    <div style="background:#020617;padding:16px;border-radius:12px;margin-bottom:20px;border:1px solid #334155;">
      <strong>Autonomous Execution Plan:</strong><br>{action_plan}
    </div>
    <a href="/store" class="btn">🚀 Explore AI Micro-Store (Starts at ₹29)</a>
    <br><br>
    <a href="/" style="color:#60a5fa;font-size:13px;">← Back to aIValue8 Home</a>
  </div>
</body>
</html>"""

def get_dynamic_seo_page(slug: str) -> str:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Match slug against opportunity titles
            cur.execute("SELECT title, action_plan, category FROM opportunities WHERE LOWER(REPLACE(REPLACE(title, ' ', '-'), '—', '')) LIKE %s LIMIT 1;", (f"%{slug}%",))
            row = cur.fetchone()
            if not row:
                # Fallback default SEO page
                return SEO_PAGE_TEMPLATE.format(
                    title="AI-Powered Business Automation & Growth Services",
                    description="Discover cutting-edge AI solutions, virtual office software, ATS resumes and automated local business growth tools.",
                    action_plan="1. Select your required micro-service.\n2. Complete instant UPI checkout.\n3. Autonomous AI delivers your digital asset instantly."
                )
            return SEO_PAGE_TEMPLATE.format(
                title=row["title"],
                description=f"Automated execution roadmap for {row['title']} powered by aIValue8 Corporation.",
                action_plan=row["action_plan"]
            )
    finally:
        conn.close()
