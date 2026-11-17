PUBLIC_HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Corporation — Live Autonomous AI OS</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    body { background: #030712; color: #e2e8f0; line-height: 1.6; overflow-x: hidden; position: relative; }
    #aiCanvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; opacity: 0.55; }
    .container { position: relative; z-index: 1; max-width: 920px; margin: 0 auto; padding: 20px 16px 40px; }
    .logo-wrap { margin-bottom: 16px; }
    .logo-wrap img { width: 100%; max-width: 630px; height: auto; display: block; border-radius: 18px; border: 1px solid rgba(56,189,248,0.25); box-shadow: 0 0 35px rgba(37,99,235,0.2); }
    .pulse-bar { display: inline-flex; align-items: center; gap: 8px; background: rgba(16,185,129,0.1); border: 1px solid rgba(52,211,153,0.35); color: #34d399; padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; margin-bottom: 14px; }
    .dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.8); } 70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
    .hero-title { font-size: 27px; font-weight: 800; color: #f8fafc; margin-bottom: 8px; min-height: 40px; }
    .typed { background: linear-gradient(90deg, #38bdf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .cursor { display: inline-block; width: 3px; height: 25px; background: #34d399; vertical-align: middle; animation: blink 0.8s infinite; margin-left: 3px; }
    @keyframes blink { 50% { opacity: 0; } }
    .hero-sub { color: #94a3b8; font-size: 14.5px; margin-bottom: 20px; }

    /* Live Telemetry Counters */
    .telemetry { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 22px; }
    .t-card { background: rgba(15,23,42,0.8); border: 1px solid #1e293b; border-radius: 12px; padding: 12px; text-align: center; }
    .t-num { font-size: 22px; font-weight: 800; color: #38bdf8; }
    .t-lbl { font-size: 11.5px; color: #94a3b8; margin-top: 2px; }

    /* Visual Automation Pipeline */
    .glass-box { background: rgba(15,23,42,0.78); backdrop-filter: blur(14px); border: 1px solid rgba(56,189,248,0.3); border-radius: 18px; padding: 18px; margin-bottom: 24px; box-shadow: 0 0 35px rgba(37,99,235,0.12); }
    .box-head { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }
    .box-head h2 { font-size: 18px; color: #f8fafc; }
    .sim-btn { background: rgba(56,189,248,0.15); border: 1px solid #38bdf8; color: #38bdf8; padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; cursor: pointer; }
    .pipeline { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-bottom: 14px; }
    .node { background: #020617; border: 1px solid #1e293b; border-radius: 12px; padding: 12px 8px; text-align: center; transition: all 0.35s ease; position: relative; }
    .node .ico { font-size: 20px; display: block; margin-bottom: 4px; }
    .node .n-title { font-size: 12px; font-weight: 700; color: #cbd5e1; }
    .node .n-sub { font-size: 10.5px; color: #64748b; }
    .node.active { border-color: #10b981; background: rgba(16,185,129,0.12); box-shadow: 0 0 20px rgba(16,185,129,0.35); transform: translateY(-3px); }
    .node.active .n-title { color: #34d399; }
    .node.done { border-color: #38bdf8; }
    .pipe-log { background: #020617; border: 1px solid #1e293b; border-radius: 10px; padding: 10px 12px; font-family: monospace; font-size: 12.5px; color: #34d399; min-height: 40px; }

    /* Evaluator & Form */
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 12px; }
    .chip { background: rgba(30,41,59,0.9); border: 1px solid #334155; color: #cbd5e1; padding: 6px 12px; border-radius: 999px; font-size: 12px; cursor: pointer; }
    .chip:hover { border-color: #38bdf8; color: #38bdf8; }
    input, select, textarea { width: 100%; background: rgba(2,6,23,0.9); color: #f8fafc; border: 1px solid #334155; border-radius: 10px; padding: 12px; margin-bottom: 12px; font-size: 14px; outline: none; }
    .btn-glow { width: 100%; background: linear-gradient(90deg, #2563eb, #10b981); color: #fff; border: none; padding: 13px; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 20px rgba(16,185,129,0.3); }
    .btn-glow:disabled { opacity: 0.6; }
    .ai-result { display: none; margin-top: 16px; background: rgba(2,6,23,0.92); border: 1px solid #10b981; border-radius: 14px; padding: 16px; }
    .score-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .score-badge { background: rgba(16,185,129,0.18); color: #34d399; padding: 4px 12px; border-radius: 999px; font-weight: 800; font-size: 14px; }
    .bar-bg { width: 100%; height: 8px; background: #1e293b; border-radius: 99px; overflow: hidden; margin-bottom: 12px; }
    .bar-fill { height: 100%; background: linear-gradient(90deg, #38bdf8, #10b981); width: 0%; transition: width 0.8s ease; }
    .steps-list { margin: 10px 0 14px 18px; font-size: 13.5px; color: #cbd5e1; }
    .btn-outline { width: 100%; background: transparent; border: 1px solid #38bdf8; color: #38bdf8; padding: 10px; border-radius: 8px; font-weight: 700; cursor: pointer; }

    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 24px; }
    .card { background: rgba(15,23,42,0.72); border: 1px solid #1e293b; border-radius: 14px; padding: 16px; }
    .card h3 { font-size: 15.5px; color: #f8fafc; margin-bottom: 5px; }
    .card p { font-size: 13px; color: #94a3b8; }
    footer { text-align: center; color: #64748b; font-size: 13px; margin-top: 20px; }
    footer a { color: #60a5fa; text-decoration: none; }
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>

  <div class="container">
    <div class="logo-wrap"><img src="/logo.svg" alt="aIValue8 Corporation" /></div>
    <div class="pulse-bar"><span class="dot"></span> aIValue8 Autonomous OS Live &bull; Mark 2 Active</div>
    <div class="hero-title"><span id="typedText" class="typed"></span><span class="cursor"></span></div>
    <p class="hero-sub">Neeche dekhein hamara AI system real-time mein kaise opportunities dhundhta, verify karta aur automate karta hai.</p>

    <!-- REAL-TIME DB COUNTERS -->
    <div class="telemetry">
      <div class="t-card"><div id="statAgents" class="t-num">-</div><div class="t-lbl">Active AI Clones</div></div>
      <div class="t-card"><div id="statGov" class="t-num">-</div><div class="t-lbl">Indian Law Checks</div></div>
      <div class="t-card"><div id="statHealed" class="t-num">-</div><div class="t-lbl">Self-Healed Bugs</div></div>
      <div class="t-card"><div id="statOpps" class="t-num">-</div><div class="t-lbl">Opportunities Found</div></div>
    </div>

    <!-- LIVE VISUAL AUTOMATION PIPELINE -->
    <div class="glass-box">
      <div class="box-head">
        <h2>⚙️ Live Automation Engine (Visual Flow)</h2>
        <button class="sim-btn" onclick="runPipelineDemo()">▶ Watch Live Flow</button>
      </div>
      <div class="pipeline">
        <div id="n0" class="node"><span class="ico">🌍</span><div class="n-title">1. Signal / Lead</div><div class="n-sub">Opportunity Scan</div></div>
        <div id="n1" class="node"><span class="ico">🧬</span><div class="n-title">2. Anti-Dup</div><div class="n-sub">SHA-256 Shield</div></div>
        <div id="n2" class="node"><span class="ico">⚖️</span><div class="n-title">3. Indian Law</div><div class="n-sub">DPDP &amp; Ethics</div></div>
        <div id="n3" class="node"><span class="ico">🤖</span><div class="n-title">4. Clone Agent</div><div class="n-sub">Task Execution</div></div>
        <div id="n4" class="node"><span class="ico">📊</span><div class="n-title">5. Smart CRM</div><div class="n-sub">Hot/Warm/Cold</div></div>
        <div id="n5" class="node"><span class="ico">🛡️</span><div class="n-title">6. Self-Heal</div><div class="n-sub">24/7 Sentinel</div></div>
      </div>
      <div id="pipeLog" class="pipe-log">&gt; System Standby... Click "Watch Live Flow" ya neeche Live AI test karein.</div>
    </div>

    <!-- LIVE AI EVALUATOR -->
    <div class="glass-box">
      <h2>⚡ Live AI Business &amp; Tech Evaluator (Free Demo)</h2>
      <div class="chips">
        <span class="chip" onclick="fillDemo('Mujhe apne business ke liye ek custom website aur WhatsApp CRM automation chahiye.')">💻 Web/App + CRM</span>
        <span class="chip" onclick="fillDemo('Main wholesale B2B buyer aur seller network badhana chahta hoon AI automation se.')">🤝 Purchase/Sell Growth</span>
        <span class="chip" onclick="fillDemo('Mujhe apni company ka social media marketing aur customer support 24/7 automate karna hai.')">🤖 24/7 AI Automation</span>
      </div>
      <textarea id="ideaInput" rows="2" placeholder="Apna business idea, website/app need ya trading requirement likhein..."></textarea>
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
      <div class="card"><h3>📈 Business Growth Engine</h3><p>Live market scanning &amp; daily venture ideas to scale revenue.</p></div>
      <div class="card"><h3>💻 Website &amp; App Build</h3><p>High-speed web platforms, dashboards &amp; mobile-ready business apps.</p></div>
      <div class="card"><h3>⚙️ End-to-End Automation</h3><p>Zero manual work—automated workflows, billing &amp; instant alerts.</p></div>
      <div class="card"><h3>📊 Smart WhatsApp CRM</h3><p>Hot/Warm/Cold lead tracking aur automated client follow-ups.</p></div>
      <div class="card"><h3>🤝 Purchase &amp; Sell Support</h3><p>Verified B2B buyer-seller matching aur safe deal coordination.</p></div>
    </div>

    <!-- CONNECT FORM -->
    <div class="glass-box" id="connectBox" style="border-color:#1e293b;">
      <h2 style="margin-bottom:6px;">📩 Start Your Project / Business Inquiry</h2>
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
    // 1. Neural Network Canvas
    const canvas = document.getElementById('aiCanvas'), ctx = canvas.getContext('2d');
    let particles = [];
    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resizeCanvas); resizeCanvas();
    for (let i = 0; i < 34; i++) particles.push({ x: Math.random()*canvas.width, y: Math.random()*canvas.height, vx: (Math.random()-0.5)*0.6, vy: (Math.random()-0.5)*0.6 });
    function animate() {
      ctx.clearRect(0,0,canvas.width,canvas.height);
      for (let i=0; i<particles.length; i++) {
        let p = particles[i]; p.x += p.vx; p.y += p.vy;
        if (p.x<0||p.x>canvas.width) p.vx*=-1; if (p.y<0||p.y>canvas.height) p.vy*=-1;
        ctx.fillStyle='#38bdf8'; ctx.beginPath(); ctx.arc(p.x,p.y,1.8,0,Math.PI*2); ctx.fill();
        for (let j=i+1; j<particles.length; j++) {
          let p2=particles[j], d=Math.hypot(p.x-p2.x,p.y-p2.y);
          if (d<130) { ctx.strokeStyle=`rgba(52,211,153,${1-d/130})`; ctx.lineWidth=0.6; ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }
        }
      }
      requestAnimationFrame(animate);
    }
    animate();

    // 2. Typing Headline
    const phrases = ["We Build AI & Automation.", "We Build Websites & Apps.", "We Power Smart CRM.", "We Scale Purchase & Sell Trade."];
    let pIdx=0, cIdx=0, del=false;
    function typeLoop() {
      const cur = phrases[pIdx], el = document.getElementById('typedText');
      if (!del) { el.textContent = cur.slice(0, ++cIdx); if (cIdx === cur.length) { del=true; setTimeout(typeLoop, 1500); return; } }
      else { el.textContent = cur.slice(0, --cIdx); if (cIdx === 0) { del=false; pIdx=(pIdx+1)%phrases.length; } }
      setTimeout(typeLoop, del ? 35 : 65);
    }
    typeLoop();

    // 3. Load Live DB Telemetry
    async function loadTelemetry() {
      try {
        const res = await fetch('/public/telemetry');
        const d = await res.json();
        document.getElementById('statAgents').textContent = d.active_agents ?? 0;
        document.getElementById('statGov').textContent = d.governance_checks ?? 0;
        document.getElementById('statHealed').textContent = d.healed_bugs ?? 0;
        document.getElementById('statOpps').textContent = d.opportunities_found ?? 0;
      } catch(e) {}
    }
    loadTelemetry();

    // 4. Visual Automation Pipeline Animator
    const stepLogs = [
      "> [Node 1] Live Opportunity / Client Signal detected...",
      "> [Node 2] SHA-256 Anti-Duplication Shield: Unique ✓ (Zero Duplicates)",
      "> [Node 3] Indian Governance Check (DPDP Act 2023 & Ethics): APPROVED ✓",
      "> [Node 4] Spawning Specialized AI Clone Agent to execute task...",
      "> [Node 5] Updating Smart CRM (Hot/Warm/Cold) & Owner Alert...",
      "> [Node 6] Sentinel Watchdog Verified — 100% Self-Healed & Ready! 🚀"
    ];
    let pipeRunning = false;
    function runPipelineDemo() {
      if (pipeRunning) return;
      pipeRunning = true;
      for (let i=0; i<6; i++) document.getElementById('n'+i).className = 'node';
      let step = 0;
      const iv = setInterval(() => {
        if (step > 0) document.getElementById('n'+(step-1)).className = 'node done';
        if (step < 6) {
          document.getElementById('n'+step).className = 'node active';
          document.getElementById('pipeLog').textContent = stepLogs[step];
          step++;
        } else {
          clearInterval(iv);
          pipeRunning = false;
        }
      }, 700);
    }
    setTimeout(runPipelineDemo, 1200);

    // 5. AI Evaluator
    function fillDemo(txt) { document.getElementById('ideaInput').value = txt; }
    async function runEvaluator() {
      const idea = document.getElementById('ideaInput').value.trim();
      const errEl = document.getElementById('evalErr'), btn = document.getElementById('evalBtn'), box = document.getElementById('aiResult');
      errEl.textContent = '';
      if (idea.length < 8) { errEl.textContent = 'Kripya kam se kam 1 line mein apni zaroorat likhein.'; return; }
      btn.disabled = true; btn.textContent = '🧠 aIValue8 AI Analyze Kar Raha Hai...'; box.style.display = 'none';
      runPipelineDemo();
      try {
        const res = await fetch('/public/evaluate', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({business_idea: idea}) });
        const data = await res.json();
        if (!res.ok) { errEl.textContent = '⚠️ ' + (data.detail || 'Evaluation error.'); }
        else {
          document.getElementById('resCategory').textContent = data.category || 'AI Solution';
          const score = Math.min(100, Math.max(50, parseInt(data.growth_score || 88)));
          document.getElementById('resScore').textContent = 'Growth Score: ' + score + '/100';
          document.getElementById('resSummary').textContent = data.summary || '';
          document.getElementById('resTime').textContent = data.launch_time || '7-14 Days';
          const ul = document.getElementById('resSteps'); ul.innerHTML = '';
          (data.steps || []).forEach(s => { const li = document.createElement('li'); li.textContent = s; ul.appendChild(li); });
          box.style.display = 'block';
          setTimeout(() => { document.getElementById('scoreBar').style.width = score + '%'; }, 100);
          loadTelemetry();
        }
      } catch(e) { errEl.textContent = '❌ Server error.'; }
      btn.disabled = false; btn.textContent = '⚡ Evaluate With aIValue8 AI';
    }

    function sendPlanToForm() {
      document.getElementById('requirement').value = `[${document.getElementById('resCategory').textContent}] ${document.getElementById('ideaInput').value.trim()}`;
      document.getElementById('connectBox').scrollIntoView({behavior:'smooth'});
      document.getElementById('name').focus();
    }

    // 6. Inquiry Form
    document.getElementById('inquiryForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn'), msg = document.getElementById('msg');
      btn.disabled = true; msg.style.color = '#94a3b8'; msg.textContent = 'aIValue8 CRM mein save ho raha hai...';
      runPipelineDemo();
      try {
        const res = await fetch('/public/inquiry', {
          method: 'POST', headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
            lead_name: document.getElementById('name').value,
            contact: document.getElementById('contact').value,
            lead_type: document.getElementById('lead_type').value,
            requirement: document.getElementById('requirement').value
          })
        });
        const data = await res.json();
        if (data.status === 'saved') { msg.style.color='#34d399'; msg.textContent='✅ Dhanyawad! Aapki detail CRM mein save ho gayi hai.'; e.target.reset(); loadTelemetry(); }
        else if (data.status === 'duplicate_skipped') { msg.style.color='#fbbf24'; msg.textContent='ℹ️ Detail pehle se registered hai.'; }
        else { msg.style.color='#f87171'; msg.textContent='⚠️ ' + (data.reason || data.message || 'Submit nahi ho saka.'); }
      } catch(err) { msg.style.color='#f87171'; msg.textContent='❌ Network error.'; }
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
    button { background: #2563eb; color: #fff; border: none; padding: 10px 14px; border-radius: 8px; font-weight: 600; cursor: pointer; margin-right: 8px; margin-bottom: 6px; }
    button.green { background: #059669; }
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
      <div class="brand-mini"><img src="/icon.svg" alt="icon" /><h1>aIValue8 Owner Room</h1></div>
      <a href="/">← Public Page</a>
    </div>

    <div id="authBox" class="login-box">
      <input type="password" id="adminKey" placeholder="Apna AIVALUE8_ADMIN_KEY daalein..." />
      <button onclick="loadDashboard()">Unlock Control Room</button>
      <div id="authErr" style="color:#f87171;margin-top:8px;font-size:13px;"></div>
    </div>

    <div id="dash" class="hidden">
      <div class="section">
        <h3 style="margin-bottom:10px;">⚡ Quick AI Controls</h3>
        <button onclick="triggerAction('/hunter/scan', 'Scanning live market...')">🌍 Run Opportunity Scan</button>
        <button class="green" onclick="triggerAction('/hunter/daily-venture', 'Creating Daily Venture idea...')">💡 Generate Daily Venture</button>
        <div id="actionRes" class="item hidden"></div>
      </div>

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
        <h3>🌍 Discovered Opportunities &amp; Daily Ventures</h3>
        <div id="oppsList"></div>
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
    if (savedKey) { document.getElementById('adminKey').value = savedKey; loadDashboard(); }

    async function loadDashboard() {
      const key = document.getElementById('adminKey').value.trim(), errBox = document.getElementById('authErr');
      errBox.textContent = '';
      try {
        const res = await fetch('/dashboard', { headers: { 'x-admin-key': key } });
        if (!res.ok) { errBox.textContent = '❌ Galat Admin Key!'; return; }
        savedKey = key; sessionStorage.setItem('av8_key', key);
        const data = await res.json();
        document.getElementById('authBox').classList.add('hidden');
        document.getElementById('dash').classList.remove('hidden');

        const wg = document.getElementById('walletsGrid'); wg.innerHTML = '';
        (data.wallets || []).forEach(w => {
          const d = document.createElement('div'); d.className = 'wallet-card';
          const t = document.createElement('div'); t.style.fontSize='12px'; t.style.color='#94a3b8';
          t.textContent = w.display_name + ' (' + w.allocation_percent + '%)';
          const a = document.createElement('div'); a.className='amt'; a.textContent = '₹' + w.balance_inr;
          d.appendChild(t); d.appendChild(a); wg.appendChild(d);
        });

        renderList('oppsList', data.recent_opportunities, o => `[${o.score}/100 | ${o.category}] ${o.title} — ${o.action_plan}`, 'Abhi koi opportunity scan nahi hui.');
        renderList('agentsList', data.clone_agents, a => `${a.agent_name} [${a.department}] — ${a.status} (Tasks: ${a.tasks_completed})`, 'Koi clone agent nahi hai.');
        renderList('leadsList', data.recent_leads, l => `[${l.temperature}] ${l.lead_name} (${l.contact}) — ${l.requirement}`, 'Abhi koi lead nahi aayi.');
        renderList('logsList', data.sentinel_logs, s => `[${s.healed ? 'HEALED' : 'ALERT'}] ${s.module}: ${s.error_text.slice(0, 120)}`, 'Koi error log nahi hai.');
      } catch(e) { errBox.textContent = '❌ Server se connect nahi ho saka.'; }
    }

    function renderList(elId, arr, formatter, emptyText) {
      const el = document.getElementById(elId); el.innerHTML = '';
      if (!arr || arr.length === 0) { const d = document.createElement('div'); d.className='item'; d.textContent=emptyText; el.appendChild(d); return; }
      arr.forEach(item => { const d = document.createElement('div'); d.className='item'; d.textContent=formatter(item); el.appendChild(d); });
    }

    async function triggerAction(endpoint, waitMsg) {
      const box = document.getElementById('actionRes'); box.classList.remove('hidden'); box.textContent = waitMsg;
      const res = await fetch(endpoint, { method: 'POST', headers: { 'x-admin-key': savedKey } });
      const data = await res.json();
      box.textContent = JSON.stringify(data, null, 2);
      loadDashboard();
    }

    async function askCeo() {
      const prompt = document.getElementById('ceoPrompt').value.trim(); if (!prompt) return;
      const box = document.getElementById('ceoReply'); box.classList.remove('hidden'); box.textContent = 'Soch raha hai...';
      const res = await fetch('/ask', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({user_message: prompt, source: 'owner-panel'}) });
      const data = await res.json(); box.textContent = data.reply || data.detail || 'Error';
    }
  </script>
</body>
</html>"""
