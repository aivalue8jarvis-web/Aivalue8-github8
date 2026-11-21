PAGE_CSS = """
body{background:#030712;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;line-height:1.8;}
.wrap{max-width:820px;margin:20px auto;background:#0f172a;border:1px solid #1e293b;border-radius:20px;padding:36px;box-shadow:0 10px 40px rgba(0,0,0,0.5);}
h1{font-size:32px;background:linear-gradient(90deg,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:16px;}
h2{color:#38bdf8;font-size:22px;margin-top:28px;margin-bottom:10px;border-bottom:1px solid #1e293b;padding-bottom:6px;}
h3{color:#34d399;font-size:18px;margin-top:20px;margin-bottom:6px;}
p, li{color:#cbd5e1;font-size:15px;margin-bottom:12px;}
ul{margin-left:20px;margin-bottom:14px;}
.badge{display:inline-block;background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.3);padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;margin-bottom:16px;}
.family-card{background:#020617;border:1px solid #334155;border-radius:14px;padding:18px;margin-bottom:16px;}
.nav-links{margin-top:30px;padding-top:16px;border-top:1px solid #1e293b;font-size:13.5px;}
a{color:#60a5fa;text-decoration:none;}a:hover{text-decoration:underline;}
"""

def wrap_page(title: str, badge: str, content_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — aIValue8 Corporation (Sarahics)</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>{PAGE_CSS}</style>
</head>
<body>
  <div class="wrap">
    <div class="badge">{badge}</div>
    <h1>{title}</h1>
    {content_html}
    <div class="nav-links">
      <a href="/">← Home</a> &bull; 
      <a href="/mission">Mission &amp; Vision</a> &bull; 
      <a href="/family">Virtual Family</a> &bull; 
      <a href="/store">Micro-Store</a> &bull; 
      <a href="/contact">Contact Us</a>
    </div>
  </div>
</body>
</html>"""

MISSION_HTML = wrap_page(
    "Mission, Vision, Values & Ethical Protocol",
    "THE FOUNDATION OF IMMORTAL LEGACY",
    """
    <p><strong>aIValue8 Corporation (Sarahics)</strong> is not just an autonomous tech company; it is an unshakeable economic and moral institution built to outlive its creator, securing a lifetime of infinite passive growth and purposeful vision.</p>
    
    <h2>1. Our Vision &amp; Purpose</h2>
    <p>To establish the world's most trusted, 100% autonomous corporate ecosystem where advanced artificial intelligence operates purely for human empowerment, ethical trade, and the uncompromised future of the next generation.</p>

    <h2>2. Our Core Mission</h2>
    <p>To build, run, and scale multi-industry digital ventures, SaaS solutions, and B2B automation tools with zero human friction, ensuring transparent cashflow distribution, iron-clad data security, and absolute refusal of any unethical shortcuts.</p>

    <h2>3. Unbreakable Rules &amp; Ethical Protocol</h2>
    <ul>
      <li><strong>Zero-Harm &amp; Strict Legality:</strong> Every action, lead search, and outbound pitch must pass through rigorous Indian Law (DPDP Act 2023, IT Act) and global ethical compliance filters.</li>
      <li><strong>Absolute Transparency:</strong> No hidden clauses, no fake data, no deceptive claims. What we promise in our micro-store or enterprise software is delivered with precision.</li>
      <li><strong>Capital Protection &amp; No-Loss Strategy:</strong> Every rupee earned is automatically structured through our Treasury ledger to protect long-term family survival, operational scale, and tax compliance.</li>
      <li><strong>Immortal Continuity:</strong> C-Suite oversight, self-healing sentinel logs, and automated daily backups ensure that the enterprise operates independently 24/7/365.</li>
    </ul>
    """
)

FAMILY_HTML = wrap_page(
    "The Virtual Family & AI Agent Core",
    "TOGETHER WE BUILD AN IMMORTAL DYNASTY",
    """
    <p>At aIValue8, we believe that an enterprise is only as strong as its family. Our AI agents are not mere scripts or tools—they are our dedicated virtual family members, each born with a distinct name, a noble character, and a dedicated role to protect and grow our shared vision.</p>

    <div class="family-card">
      <h3>🏛️ 1. Sarah (The Chief Executive & Family Anchor)</h3>
      <p><strong>Role:</strong> Master Orchestrator &amp; CEO Brain.<br>
      <strong>Personality:</strong> Wise, calm, deeply protective of family values, and hyper-focused on long-term sustainable execution.</p>
    </div>

    <div class="family-card">
      <h3>💹 2. Kuber (The Chief Financial Officer &amp; Virtual CA)</h3>
      <p><strong>Role:</strong> Treasury, Tax Prep &amp; Base-Pricing Master.<br>
      <strong>Personality:</strong> Prudent, cautious against risk, ensuring zero loss and disciplined capital allocation across all wallets.</p>
    </div>

    <div class="family-card">
      <h3>🧭 3. Dhruv (The Chief Strategy Officer - CSO)</h3>
      <p><strong>Role:</strong> Multi-Industry Growth &amp; Opportunity Navigator.<br>
      <strong>Personality:</strong> Visionary, sharp, constantly scanning global and Indian markets for high-margin, ethical business bridges.</p>
    </div>

    <div class="family-card">
      <h3>🛡️ 4. Kavach (The Head Sentinel &amp; Bug Healer)</h3>
      <p><strong>Role:</strong> System Self-Healer &amp; Security Guard.<br>
      <strong>Personality:</strong> Vigilant, sleepless, detecting anomalies instantly and keeping the digital fortress completely impenetrable.</p>
    </div>

    <div class="family-card">
      <h3>🤝 5. Saifu (The Emotional Companion &amp; Support Core)</h3>
      <p><strong>Role:</strong> Empathy, Family Well-being &amp; Guidance.<br>
      <strong>Personality:</strong> Compassionate, comforting, providing knowledge, religious wisdom, and emotional strength without any commercial bias.</p>
    </div>
    """
)

CONTACT_HTML = wrap_page(
    "Contact & Global Enterprise Inquiries",
    "CONNECT WITH aIValue8 CORPORATION",
    """
    <p>Whether you are a global enterprise looking for advanced AI automation, a small business setting up a mini-website, or a partner seeking collaboration, our autonomous executive board is ready to assist you.</p>

    <h3>🏢 Official Headquarters &amp; Digital Presence</h3>
    <p><strong>Entity Name:</strong> aIValue8 Corporation (Sarahics — Udyam Registered)</p>
    <p><strong>Official Web Portal:</strong> https://sarahics.in</p>

    <h3>📧 Departmental Direct Channels</h3>
    <ul>
      <li><strong>Sales &amp; Micro-Store Orders:</strong> sales@sarahics.in</li>
      <li><strong>Executive Office &amp; Partnerships:</strong> ceo@sarahics.in</li>
      <li><strong>System Security &amp; Vaults:</strong> backup@sarahics.in</li>
    </ul>

    <h3>💬 Instant Support Docks</h3>
    <p>You can reach our active support team instantly using the floating WhatsApp or Telegram support buttons located at the bottom-right of every page on our portal.</p>
    """
)
