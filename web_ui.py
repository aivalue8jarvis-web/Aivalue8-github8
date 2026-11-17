PUBLIC_HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Corporation — AI, Automation, Web/App, CRM &amp; Business Growth</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    body { background: #050811; color: #e2e8f0; line-height: 1.6; padding: 18px; }
    .container { max-width: 860px; margin: 0 auto; }
    .logo-wrap { margin-bottom: 18px; }
    .logo-wrap img { width: 100%; max-width: 630px; height: auto; display: block; border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 600; margin-bottom: 18px; }
    .dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 28px; }
    .card { background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; padding: 18px; }
    .card h3 { font-size: 16px; color: #f8fafc; margin-bottom: 6px; }
    .card p { font-size: 13px; color: #94a3b8; }
    .form-box { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 22px; margin-bottom: 24px; }
    .form-box h2 { font-size: 20px; margin-bottom: 6px; color: #f8fafc; }
    .form-box small { display: block; color: #94a3b8; margin-bottom: 16px; }
    input, select, textarea { width: 100%; background: #020617; color: #f8fafc; border: 1px solid #334155; border-radius: 10px; padding: 12px; margin-bottom: 12px; font-size: 14px; }
    button { width: 100%; background: linear-gradient(90deg, #2563eb, #10b981); color: white; border: none; padding: 13px; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; }
    button:disabled { opacity: 0.6; }
    #msg { margin-top: 12px; font-size: 14px; font-weight: 600; }
    footer { text-align: center; color: #64748b; font-size: 13px; margin-top: 24px; }
    footer a { color: #60a5fa; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo-wrap">
      <img src="/logo.svg" alt="aIValue8 Corporation Logo" />
    </div>
    <div class="badge"><span class="dot"></span> System Live 24/7 &bull; Ethical Indian AI Governance</div>

    <div class="grid">
      <div class="card">
        <h3>🤖 AI &amp; Automation</h3>
        <p>Custom AI agents, 24/7 automated workflows, and self-healing business operations.</p>
      </div>
      <div class="card">
        <h3>💻 Website &amp; App Build</h3>
        <p>Fast, scalable websites, web apps, and custom business software tailored for growth.</p>
      </div>
      <div class="card">
        <h3>🤝 CRM &amp; Purchase/Sell Support</h3>
        <p>Smart buyer-seller matching, lead tracking, automated follow-ups &amp; deal closing.</p>
      </div>
    </div>

    <div class="form-box">
      <h2>📩 Connect / Business Inquiry</h2>
      <small>Website/App banwana ho, AI Automation chahiye, ya Buyer/Seller Support — apni detail bhejein:</small>
      <form id="inquiryForm">
        <input type="text" id="name" placeholder="Aapka Naam / Company Name" required />
        <input type="text" id="contact" placeholder="WhatsApp Number ya Email" required />
        <select id="lead_type">
          <option value="BUYER">Product / Service Chahiye (Web, App, AI, Purchase)</option>
          <option value="SELLER">Main Seller / Supplier hoon</option>
          <option value="PARTNER">Business Growth / Partnership</option>
        </select>
        <textarea id="requirement" rows="3" placeholder="Aapki requirement ya business idea likhein..." required></textarea>
        <button type="submit" id="submitBtn">Submit to aIValue8</button>
      </form>
      <div id="msg"></div>
    </div>

    <footer>
      <strong>aIValue8 Corporation</strong> &bull; <a href="/icon.svg" target="_blank">App Icon</a> &bull; <a href="/logo.svg" target="_blank">HD Logo</a> &bull; <a href="/panel">Owner Control Room</a>
    </footer>
  </div>

  <script>
    document.getElementById('inquiryForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      const msg = document.getElementById('msg');
      btn.disabled = true;
      msg.style.color = '#94a3b8';
      msg.textContent = 'aIValue8 evaluate kar raha hai...';
      try {
        const res = await fetch('/public/inquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            lead_name: document.getElementById('name').value,
            contact: document.getElementById('contact').value,
            lead_type: document.getElementById('lead_type').value,
            requirement: document.getElementById('requirement').value
          })
        });
        const data = await res.json();
        if (data.status === 'saved') {
          msg.style.color = '#34d399';
          msg.textContent = '✅ Dhanyawad! Aapki inquiry aIValue8 CRM mein save ho gayi hai. Hamari team jald sampark karegi.';
          e.target.reset();
        } else if (data.status === 'duplicate_skipped') {
          msg.style.color = '#fbbf24';
          msg.textContent = 'ℹ️ Aapki detail pehle se hamare system mein registered hai.';
        } else {
          msg.style.color = '#f87171';
          msg.textContent = '⚠️ ' + (data.reason || data.message || 'Submit nahi ho saka.');
        }
      } catch (err) {
        msg.style.color = '#f87171';
        msg.textContent = '❌ Network error, kripya dubara try karein.';
      }
      btn.disabled = false;
    });
  </script>
</body>
</html>"""

OWNER_PANEL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 — Owner Control Room</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    body { background: #020617; color: #e2e8f0; padding: 18px; }
    .wrap { max-width: 900px; margin: 0 auto; }
    h1 { font-size: 22px; color: #38bdf8; }
    .login-box, .section { background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; padding: 16px; margin-bottom: 16px; }
    input, textarea { width: 100%; background: #020617; color: #fff; border: 1px solid #334155; border-radius: 8px; padding: 10px; margin-bottom: 10px; }
    button { background: #2563eb; color: #fff; border: none; padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; }
    .wallet-card { background: #020617; border: 1px solid #1e293b; border-radius: 10px; padding: 12px; }
    .wallet-card .amt { font-size: 20px; font-weight: 800; color: #34d399; margin-top: 4px; }
    .item { background: #020617; border: 1px solid #1e293b; border-radius: 8px; padding: 10px; margin-top: 8px; font-size: 13px; }
    .hidden { display: none; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
    .brand-mini { display: flex; align-items: center; gap: 10px; }
    .brand-mini img { width: 34px; height: 34px; border-radius: 8px; }
    a { color: #94a3b8; font-size: 13px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top-bar">
      <div class="brand-mini">
        <img src="/icon.svg" alt="icon" />
        <h1>aIValue8 Owner Room</h1>
      </div>
      <a href="/">← Public Page</a>
    </div>

    <div id="authBox" class="login-box">
      <input type="password" id="adminKey" placeholder="Apna AIVALUE8_ADMIN_KEY daalein..." />
      <button onclick="loadDashboard()">Unlock Control Room</button>
      <div id="authErr" style="color:#f87171;margin-top:8px;font-size:13px;"></div>
    </div>

    <div id="dash" class="hidden">
      <div class="section">
        <h3 style="margin-bottom:10px;">💰 Treasury &amp; Wallets</h3>
        <div id="walletsGrid" class="grid"></div>
      </div>

      <div class="section">
        <h3 style="margin-bottom:10px;">🧠 Talk to aIValue8 CEO</h3>
        <textarea id="ceoPrompt" rows="2" placeholder="CEO se koi sawal ya command poochhein..."></textarea>
        <button onclick="askCeo()">Send to CEO</button>
        <div id="ceoReply" class="item hidden"></div>
      </div>

      <div class="section">
        <h3>🧬 Active Clone Agents</h3>
        <div id="agentsList"></div>
      </div>

      <div class="section">
        <h3>📋 Recent CRM Leads</h3>
        <div id="leadsList"></div>
      </div>

      <div class="section">
        <h3>🛡️ Sentinel Self-Healing Logs</h3>
        <div id="logsList"></div>
      </div>
    </div>
  </div>

  <script>
    let savedKey = sessionStorage.getItem('av8_key') || '';
    if (savedKey) {
      document.getElementById('adminKey').value = savedKey;
      loadDashboard();
    }

    async function loadDashboard() {
      const key = document.getElementById('adminKey').value.trim();
      const errBox = document.getElementById('authErr');
      errBox.textContent = '';
      try {
        const res = await fetch('/dashboard', { headers: { 'x-admin-key': key } });
        if (!res.ok) {
          errBox.textContent = '❌ Galat Admin Key!';
          return;
        }
        savedKey = key;
        sessionStorage.setItem('av8_key', key);
        const data = await res.json();
        document.getElementById('authBox').classList.add('hidden');
        document.getElementById('dash').classList.remove('hidden');

        const wg = document.getElementById('walletsGrid');
        wg.innerHTML = '';
        (data.wallets || []).forEach(w => {
          const d = document.createElement('div');
          d.className = 'wallet-card';
          const title = document.createElement('div');
          title.style.fontSize = '12px';
          title.style.color = '#94a3b8';
          title.textContent = w.display_name + ' (' + w.allocation_percent + '%)';
          const amt = document.createElement('div');
          amt.className = 'amt';
          amt.textContent = '₹' + w.balance_inr;
          d.appendChild(title);
          d.appendChild(amt);
          wg.appendChild(d);
        });

        renderList('agentsList', data.clone_agents, a => `${a.agent_name} [${a.department}] — ${a.status} (Tasks: ${a.tasks_completed})`, 'Koi clone agent nahi hai.');
        renderList('leadsList', data.recent_leads, l => `[${l.temperature}] ${l.lead_name} (${l.contact}) — ${l.requirement}`, 'Abhi koi lead nahi aayi.');
        renderList('logsList', data.sentinel_logs, s => `[${s.healed ? 'HEALED' : 'ALERT'}] ${s.module}: ${s.error_text.slice(0, 120)}`, 'Koi error log nahi hai.');
      } catch (e) {
        errBox.textContent = '❌ Server se connect nahi ho saka.';
      }
    }

    function renderList(elId, arr, formatter, emptyText) {
      const el = document.getElementById(elId);
      el.innerHTML = '';
      if (!arr || arr.length === 0) {
        const d = document.createElement('div');
        d.className = 'item';
        d.textContent = emptyText;
        el.appendChild(d);
        return;
      }
      arr.forEach(item => {
        const d = document.createElement('div');
        d.className = 'item';
        d.textContent = formatter(item);
        el.appendChild(d);
      });
    }

    async function askCeo() {
      const prompt = document.getElementById('ceoPrompt').value.trim();
      if (!prompt) return;
      const box = document.getElementById('ceoReply');
      box.classList.remove('hidden');
      box.textContent = 'Soch raha hai...';
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: prompt, source: 'owner-panel' })
      });
      const data = await res.json();
      box.textContent = data.reply || data.detail || 'Error';
    }
  </script>
</body>
</html>"""
