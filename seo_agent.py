import os
import re
import json
from database import get_connection
from sentinel import smart_generate, send_alert, PRIMARY_MODEL
from governance import check_compliance
from cloner import register_unique_or_reject

PUBLIC_URL = os.getenv("PUBLIC_SITE_URL", "https://sarahics.in").rstrip("/")

def run_seo_keyword_agent() -> dict:
    prompt = f"""
    Tum aIValue8 (Website: {PUBLIC_URL}) ke Senior Google SEO Strategist ho.
    India ke small businesses, students, CA firms ya startups ke liye 1 aisa high-intent, low-competition Google Search Keyword chuno jo hamari services (₹29 ATS Resume, ₹99 Shop Mini-Website/QR Menu, ₹49 Digital Virtual Office, AI Automation, B2B Trade) se match kare.
    Us keyword par ek genuinely helpful, zero-spam HTML guide + 3 FAQs + CTA link to {PUBLIC_URL}/store banao.
    Reply ONLY valid JSON:
    {{
      "keyword": "target long-tail keyword",
      "slug": "clean-url-slug-in-lowercase",
      "title": "SEO Page Title under 60 chars",
      "meta_desc": "Compelling 140-char Google meta description",
      "faq_list": [{{"q": "Question 1?", "a": "Clear helpful answer."}}, {{"q": "Question 2?", "a": "Answer 2."}}],
      "article_html": "<h3>...</h3><p>Detailed 3-paragraph helpful guide in simple English/Hinglish...</p>"
    }}
    """
    data = json.loads(smart_generate(prompt, system_prompt="Tum Google Search SEO Expert ho.", model=PRIMARY_MODEL, json_mode=True))
    raw_slug = data.get("slug") or data.get("keyword") or "ai-business-india"
    slug = re.sub(r"[^a-z0-9]+", "-", raw_slug.lower()).strip("-")[:70]
    title = (data.get("title") or data.get("keyword") or "aIValue8 Guide").strip()

    if not slug or not register_unique_or_reject("SEO_PAGE", slug, title):
        return {"status": "duplicate_skipped", "slug": slug}

    gov = check_compliance("SEO_PAGE", f"{title} | {data.get('article_html', '')}")
    if not gov["approved"]:
        return {"status": "blocked_by_governance", "reason": gov["reason"]}

    faqs = data.get("faq_list", [])
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f.get("q", ""), "acceptedAnswer": {"@type": "Answer", "text": f.get("a", "")}} for f in faqs if f.get("q")]
    }
    faq_html = "".join([f"<div style='margin:12px 0;padding:12px;background:#020617;border-radius:10px;'><strong>Q: {f.get('q','')}</strong><br><span style='color:#94a3b8;'>{f.get('a','')}</span></div>" for f in faqs])

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — aIValue8 (Sarahics)</title>
  <meta name="description" content="{data.get('meta_desc', title)}" />
  <meta name="keywords" content="{data.get('keyword', '')}, aIValue8, Sarahics, AI Automation India" />
  <link rel="canonical" href="{PUBLIC_URL}/p/{slug}" />
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
  <style>body{{background:#030712;color:#e2e8f0;font-family:sans-serif;padding:20px;line-height:1.7;}}.w{{max-width:780px;margin:0 auto;background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:26px;}}h1{{color:#38bdf8;margin-bottom:10px;}}h3{{color:#34d399;margin:16px 0 8px;}}p{{color:#cbd5e1;margin-bottom:12px;}}.btn{{display:inline-block;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;padding:12px 22px;border-radius:10px;text-decoration:none;font-weight:700;margin-top:12px;}}</style>
</head>
<body>
  <div class="w">
    <span style="color:#34d399;font-size:12px;font-weight:700;">KEYWORD: {data.get('keyword','')}</span>
    <h1>{title}</h1>
    {data.get('article_html', '')}
    <h3>Frequently Asked Questions</h3>
    {faq_html}
    <a href="/store" class="btn">🚀 Try Micro-Store (Starts at ₹29)</a>
    <p style="margin-top:18px;font-size:13px;"><a href="/" style="color:#60a5fa;">← Home</a> | <a href="/privacy" style="color:#60a5fa;">Privacy</a></p>
  </div>
</body>
</html>"""

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO client_pages (slug, client_name, page_type, html_content) VALUES (%s,%s,%s,%s) ON CONFLICT (slug) DO NOTHING;",
                    (slug, data.get("keyword", "")[:140], "SEO_GUIDE", full_html)
                )
    finally:
        conn.close()

    live_url = f"{PUBLIC_URL}/p/{slug}"
    send_alert(f"🔍 NEW GOOGLE SEO PAGE LIVE!\nKeyword: {data.get('keyword')}\n🔗 {live_url}")
    return {"status": "seo_page_live", "keyword": data.get("keyword"), "url": live_url}
