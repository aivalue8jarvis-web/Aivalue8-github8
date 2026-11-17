PUBLIC_HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Corporation — Live AI Business &amp; Automation OS</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    body { background: #030712; color: #e2e8f0; line-height: 1.6; overflow-x: hidden; position: relative; }
    #aiCanvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; opacity: 0.55; }
    .container { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 20px 16px 40px; }
    .logo-wrap { margin-bottom: 18px; }
    .logo-wrap img { width: 100%; max-width: 630px; height: auto; display: block; border-radius: 18px; border: 1px solid rgba(56,189,248,0.25); box-shadow: 0 0 35px rgba(37,99,235,0.2); }
    .pulse-bar { display: inline-flex; align-items: center; gap: 8px; background: rgba(16,185,129,0.1); border: 1px solid rgba(52,211,153,0.35); color: #34d399; padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; margin-bottom: 16px; }
    .dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.8); } 70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
    .hero-title { font-size: 28px; font-weight: 800; color: #f8fafc; margin-bottom: 8px; min-height: 40px; }
    .typed { background: linear-gradient(90deg, #38bdf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .cursor { display: inline-block; width: 3px; height: 26px; background: #34d399; vertical-align: middle; animation: blink 0.8s infinite; margin-left: 3px; }
    @keyframes blink { 50% { opacity: 0; } }
    .hero-sub { color: #94a3b8; font-size: 15px; margin-bottom: 24px; }

    /* Live AI Evaluator Box */
    .glass-box { background: rgba(15,23,42,0.78); backdrop-filter: blur(14px); border: 1px solid rgba(56,189,248,0.35); border-radius: 18px; padding: 20px; margin-bottom: 26px; box-shadow: 0 0 40px rgba(37,99,235,0.15); }
    .glass-box h2 { font-size: 19px; color: #f8fafc; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
    .glass-box small { display: block; color: #94a3b8; margin-bottom: 12px; font-size: 13px; }
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
    .chip { background: rgba(30,41,59,0.9); border: 1px solid #334155; color: #cbd5e1; padding: 6px 12px; border-radius: 999px; font-size: 12px; cursor: pointer; transition: 0.2s; }
    .chip:hover { border-color: #38bdf8; color: #38bdf8; }
    input, select, textarea { width: 100%; background: rgba(2,6,23,0.9); color: #f8fafc; border: 1px solid #334155; border-radius: 10px; padding: 12px; margin-bottom: 12px; font-size: 14px; outline: none; }
    input:focus, textarea:focus { border-color: #38bdf8; }
    .btn-glow { width: 100%; background: linear-gradient(90deg, #2563eb, #10b981); color: #fff; border: none; padding: 13px; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 20px rgba(16,185,129,0.3); transition: 0.2s; }
    .btn-glow:disabled { opacity: 0.6; }

    /* AI Result Card */
    .ai-result { display: none; margin-top: 16px; background: rgba(2,6,23,0.92); border: 1px solid #10b981; border-radius: 14px; padding: 16px; animation: fadeIn 0.4s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    .score-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .score-badge { background: rgba(16,185,129,0.18); color: #34d399; padding: 4px 12px; border-radius: 999px; font-weight: 800; font-size: 14px; }
    .bar-bg { width: 100%; height: 8px; background: #1e293b; border-radius: 99px; overflow: hidden; margin-bottom: 12px; }
    .bar-fill { height: 100%; background: linear-gradient(90deg, #38bdf8, #10b981); width: 0%; transition: width 0.8s ease; }
    .steps-list { margin: 10px 0 14px 18px; font-size: 13.5px; color: #cbd5e1; }
    .steps-list li { margin-bottom: 5px; }
    .btn-outline { width: 100%; background: transparent; border: 1px solid #38bdf8; color: #38bdf8; padding: 10px; border-radius: 8px; font-weight: 700; cursor: pointer; }

    /* 6 Services Grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 26px; }
    .card { background: rgba(15,23,42,0.72); backdrop-filter: blur(8px); border: 1px solid #1e293b; border-radius: 14px; padding: 16px; transition: 0.25s; }
    .card:hover { border-color: #38bdf8; transform: translateY(-2px); }
    .card h3 { font-size: 15.5px; color: #f8fafc; margin-bottom: 5px; }
    .card p { font-size: 13px; color: #94a3b8; }

    footer { text-align: center; color: #64748b; font-size: 13px; margin-top: 20px; }
    footer a { color: #60a5fa; text-decoration: none; }
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>

  <div class="container">
    <div class="logo-wrap">
      <img src="/logo.svg" alt="aIValue8 Corporation" />
    </div>

    <div class="pulse-bar"><span class="dot"></span> aIValue8 AI Core Live &bull; Try Interactive Demo Below</div>

    <div class="hero-title"><span id="typedText" class="typed"></span><span class="cursor"></span></div>
    <p class="hero-sub">Sirf baatein nahi—aaiye live dekhein hamara AI aapke business ko kaise automate aur grow kar sakta hai.</p>

    <!-- LIVE AI EVALUATOR -->
    <div class="glass-box">
      <h2>⚡ Live AI Business &amp; Tech Evaluator (Free Demo)</h2>
      <small>Apna business idea, website/app requirement ya trading need likhein—3 second mein AI roadmap paayein:</small>
      <div class="chips">
        <span class="chip" onclick="fillDemo('Mujhe apne business ke liye ek custom website aur WhatsApp CRM automation chahiye.')">💻 Web/App + CRM</span>
        <span class="chip" onclick="fillDemo('Main wholesale B2B buyer aur seller network badhana chahta hoon AI automation se.')">🤝 Purchase/Sell Growth</span>
        <span class="chip" onclick="fillDemo('Mujhe apni company ka social media marketing aur customer support 24/7 automate karna hai.')">🤖 24/7 AI Automation</span>
      </div>
      <textarea id="ideaInput" rows="2" placeholder="Yahan likhein: Jaise 'Mera real estate/trading ka kaam hai, leads aur follow-up automate karna hai...'"></textarea>
      <button id="evalBtn" class="btn-glow" onclick="runEvaluator()">⚡ Evaluate With aIValue8 AI</button>
      <div id="evalErr" style="color:#f87171;font-size:13px;margin-top:8px;"></div>

      <div id="aiResult" class="ai-result">
        <div class="score-row">
          <strong id="resCategory" style="color:#38bdf8;font-size:14px;">AI Strategy</strong>
          <span id="resScore" class="score-badge">90 / 100</span>
        </div>
        <div class="bar-bg"><div id="scoreBar" class="bar-fill"></div></div>
        <p id="resSummary" style="font-size:14px;color:#f8fafc;margin-bottom:8px;"></p>
        <ul id="resSteps" class="steps-list"></ul>
        <div style="font-size:12px;color:#94a3b8;margin-bottom:10px;">⏱️ Estimated Build Time: <strong id="resTime" style="color:#34d399;"></strong></div>
        <button class="btn-outline" onclick="sendPlanToForm()">🚀 Is Plan Ko Execute Karwayein (Connect Now)</button>
      </div>
    </div>

    <!-- 6 CAPABILITIES -->
    <div class="grid">
      <div class="card"><h3>🤖 Autonomous AI Agents</h3><p>24/7 kaam karne wale custom AI clones for sales, research &amp; support.</p></div>
      <div class="card"><h3>📈 Business Growth Engine</h3><p>Data-backed strategies to scale leads, conversions &amp; revenue.</p></div>
      <div class="card"><h3>💻 Website &amp; App Build</h3><p>High-speed web platforms, dashboards &amp; mobile-ready business apps.</p></div>
      <div class="card"><h3>⚙️ End-to-End Automation</h3><p>Zero manual work—automated workflows, billing &amp; instant alerts.</p></div>
      <div class="card"><h3>📊 Smart WhatsApp CRM</h3><p>Hot/Warm/Cold lead tracking aur automated client follow-ups.</p></div>
      <div class="card"><h3>🤝 Purchase &amp; Sell Support</h3><p>Verified B2B buyer-seller matching aur safe deal coordination.</p></div>
    </div>

    <!-- CONNECT FORM -->
    <div class="glass-box" id="connectBox" style="border-color:#1e293b;">
      <h2>📩 Start Your Project / Business Inquiry</h2>
      <small>Hamari AI team aur experts aapse turant WhatsApp/Email par sampark karenge.</small>
      <form id="inquiryForm">
        <input type="text" id="name" placeholder="Aapka Naam / Company Name" required />
        <input type="text" id="contact" placeholder="WhatsApp Number ya Email" required />
        <select id="lead_type">
          <option value="BUYER">Product / Service Chahiye (AI, Web/App, Automation)</option>
          <option value="SELLER">Main Seller / Supplier hoon (Purchase-Sell Support)</option>
          <option value="PARTNER">Business Growth &amp; Partnership</option>
        </select>
        <textarea id="requirement" rows="3" placeholder="Aapki requirement likhein..." required></textarea>
        <button type="submit" id="submitBtn" class="btn-glow">Submit Inquiry to aIValue8</button>
      </form>
      <div id="msg" style="margin-top:12px;font-size:14px;font-weight:600;"></div>
    </div>

    <footer>
      <strong>aIValue8 Corporation</strong> &bull; Indian Law &amp; Ethics Compliant &bull; <a href="/panel">Owner Control Room</a>
    </footer>
  </div>

  <script>
    // 1. Neural Network Canvas Animation
    const canvas = document.getElementById('aiCanvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    for (let i = 0; i < 36; i++) {
      particles.push({
        x: Math.random() * canvas.width, y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.6, vy: (Math.random() - 0.5) * 0.6
      });
    }
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath(); ctx.arc(p.x, p.y, 1.8, 0, Math.PI * 2); ctx.fill();
        for (let j = i + 1; j < particles.length; j++) {
          let p2 = particles[j];
          let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (dist < 130) {
            ctx.strokeStyle = `rgba(52, 211, 153, ${1 - dist / 130})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animate);
    }
    animate();

    // 2. Typing Headline Effect
    const phrases = [
      "We Build AI & Automation.",
      "We Build Websites & Apps.",
      "We Power Smart CRM.",
      "We Scale Purchase & Sell Trade."
    ];
    let pIdx = 0, cIdx = 0, deleting = false;
    function typeLoop() {
      const current = phrases[pIdx];
      const el = document.getElementById('typedText');
      if (!deleting) {
        el.textContent = current.slice(0, ++cIdx);
        if (cIdx === current.length) { deleting = true; setTimeout(typeLoop, 1500); return; }
      } else {
        el.textContent = current.slice(0, --cIdx);
        if (cIdx === 0) { deleting = false; pIdx = (pIdx + 1) % phrases.length; }
      }
      setTimeout(typeLoop, deleting ? 35 : 65);
    }
    typeLoop();

    // 3. Live AI Evaluator
    function fillDemo(txt) { document.getElementById('ideaInput').value = txt; }

    async function runEvaluator() {
      const idea = document.getElementById('ideaInput').value.trim();
      const errEl = document.getElementById('evalErr');
      const btn = document.getElementById('evalBtn');
      const box = document.getElementById('aiResult');
      errEl.textContent = '';
      if (idea.length < 8) { errEl.textContent = 'Kripya kam se kam 1 line mein apni zaroorat likhein.'; return; }
      btn.disabled = true;
      btn.textContent = '🧠 aIValue8 AI Analyze Kar Raha Hai...';
      box.style.display = 'none';
      try {
        const res = await fetch('/public/evaluate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ business_idea: idea })
        });
        const data = await res.json();
        if (!res.ok) {
          errEl.textContent = '⚠️ ' + (data.detail || 'Evaluation error.');
        } else {
          document.getElementById('resCategory').textContent = data.category || 'AI Solution';
          const score = Math.min(100, Math.max(50, parseInt(data.growth_score || 88)));
          document.getElementById('resScore').textContent = 'Growth Score: ' + score + '/100';
          document.getElementById('resSummary').textContent = data.summary || '';
          document.getElementById('resTime').textContent = data.launch_time || '7-14 Days';
          const ul = document.getElementById('resSteps');
          ul.innerHTML = '';
          (data.steps || []).forEach(s => {
            const li = document.createElement('li');
            li.textContent = s;
            ul.appendChild(li);
          });
          box.style.display = 'block';
          setTimeout(() => { document.getElementById('scoreBar').style.width = score + '%'; }, 100);
        }
      } catch (e) {
        errEl.textContent = '❌ Server se connect nahi ho saka.';
      }
      btn.disabled = false;
      btn.textContent = '⚡ Evaluate With aIValue8 AI';
    }

    function sendPlanToForm() {
      const idea = document.getElementById('ideaInput').value.trim();
      const cat = document.getElementById('resCategory').textContent;
      document.getElementById('requirement').value = `[${cat}] ${idea}`;
      document.getElementById('connectBox').scrollIntoView({ behavior: 'smooth' });
      document.getElementById('name').focus();
    }

    // 4. Inquiry Submit
    document.getElementById('inquiryForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      const msg = document.getElementById('msg');
      btn.disabled = true;
      msg.style.color = '#94a3b8';
      msg.textContent = 'aIValue8 CRM mein save ho raha hai...';
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
          msg.textContent = '✅ Dhanyawad! Aapki detail aIValue8 CRM mein save ho gayi hai. Hum jald contact karenge.';
          e.target.reset();
        } else if (data.status === 'duplicate_skipped') {
          msg.style.color = '#fbbf24';
          msg.textContent = 'ℹ️ Aapki detail pehle se registered hai.';
        } else {
          msg.style.color = '#f87171';
          msg.textContent = '⚠️ ' + (data.reason || data.message || 'Submit nahi ho saka.');
        }
      } catch (err) {
        msg.style.color = '#f87171';
        msg.textContent = '❌ Network error, dubara try karein.';
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
