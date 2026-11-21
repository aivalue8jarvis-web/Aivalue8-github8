import os

_raw_wa = os.getenv("WHATSAPP_SUPPORT_NUMBER", "").strip()
_digits = "".join(c for c in _raw_wa if c.isdigit())
if len(_digits) == 10:
    _digits = "91" + _digits
WA_NUMBER = _digits if len(_digits) >= 10 else "91NAYA_NUMBER"

PUBLIC_HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Corporation — AI OS, Virtual Office &amp; Automation</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#030712;color:#e2e8f0;line-height:1.6;overflow-x:hidden;position:relative;}
    #aiCanvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.55;}
    .container{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:20px 16px 85px;}
    .logo-wrap{margin-bottom:16px;}
    .logo-wrap img{width:100%;max-width:630px;height:auto;display:block;border-radius:18px;border:1px solid rgba(56,189,248,0.25);box-shadow:0 0 35px rgba(37,99,235,0.2);}
    .pulse-bar{display:inline-flex;align-items:center;gap:8px;background:rgba(16,185,129,0.1);border:1px solid rgba(52,211,153,0.35);color:#34d399;padding:6px 14px;border-radius:999px;font-size:12.5px;font-weight:700;margin-bottom:14px;}
    .dot{width:8px;height:8px;background:#10b981;border-radius:50%;animation:pulse 1.5s infinite;}
    @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,0.8);}70%{box-shadow:0 0 0 10px rgba(16,185,129,0);}100%{box-shadow:0 0 0 0 rgba(16,185,129,0);}}
    .hero-title{font-size:26px;font-weight:800;color:#f8fafc;margin-bottom:8px;min-height:38px;}
    .typed{background:linear-gradient(90deg,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .cursor{display:inline-block;width:3px;height:24px;background:#34d399;vertical-align:middle;animation:blink 0.8s infinite;margin-left:3px;}
    @keyframes blink{50%{opacity:0;}}
    .hero-sub{color:#94a3b8;font-size:14.5px;margin-bottom:18px;}
    .telemetry{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:20px;}
    .t-card{background:rgba(15,23,42,0.8);border:1px solid #1e293b;border-radius:12px;padding:12px;text-align:center;}
    .t-num{font-size:22px;font-weight:800;color:#38bdf8;}
    .t-lbl{font-size:11.5px;color:#94a3b8;margin-top:2px;}
    .glass-box{background:rgba(15,23,42,0.78);backdrop-filter:blur(14px);border:1px solid rgba(56,189,248,0.3);border-radius:18px;padding:18px;margin-bottom:20px;box-shadow:0 0 35px rgba(37,99,235,0.12);}
    .box-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:14px;}
    .box-head h2{font-size:18px;color:#f8fafc;}
    .sim-btn{background:rgba(56,189,248,0.15);border:1px solid #38bdf8;color:#38bdf8;padding:6px 14px;border-radius:999px;font-size:12.5px;font-weight:700;cursor:pointer;}
    .pipeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:8px;margin-bottom:12px;}
    .node{background:#020617;border:1px solid #1e293b;border-radius:12px;padding:10px 6px;text-align:center;transition:all 0.35s ease;}
    .node .ico{font-size:18px;display:block;margin-bottom:3px;}
    .node .n-title{font-size:11.5px;font-weight:700;color:#cbd5e1;}
    .node .n-sub{font-size:10px;color:#64748b;}
    .node.active{border-color:#10b981;background:rgba(16,185,129,0.14);box-shadow:0 0 20px rgba(16,185,129,0.35);transform:translateY(-3px);}
    .node.active .n-title{color:#34d399;}
    .node.done{border-color:#38bdf8;}
    .pipe-log{background:#020617;border:1px solid #1e293b;border-radius:10px;padding:10px 12px;font-family:monospace;font-size:12.5px;color:#34d399;min-height:40px;}
    .media-grid,.vo-grid,.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:12px;margin-bottom:16px;}
    .media-card,.vo-card,.card{background:rgba(2,6,23,0.88);border:1px solid #1e293b;border-radius:14px;padding:15px;}
    .vo-card{border-color:rgba(52,211,153,0.35);}
    .vo-price{font-size:22px;font-weight:900;color:#34d399;margin:6px 0;}
    .m-tag{display:inline-block;background:rgba(56,189,248,0.15);color:#38bdf8;font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;margin-bottom:6px;}
    .chips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 12px;}
    .chip{background:rgba(30,41,59,0.9);border:1px solid #334155;color:#cbd5e1;padding:6px 12px;border-radius:999px;font-size:12px;cursor:pointer;}
    input,select,textarea{width:100%;background:rgba(2,6,23,0.9);color:#f8fafc;border:1px solid #334155;border-radius:10px;padding:12px;margin-bottom:12px;font-size:14px;outline:none;}
    .btn-glow{width:100%;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:13px;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;}
    .btn-glow:disabled{opacity:0.6;}
    .btn-outline{width:100%;background:transparent;border:1px solid #38bdf8;color:#38bdf8;padding:9px;border-radius:8px;font-weight:700;cursor:pointer;margin-top:8px;}
    .ai-result{display:none;margin-top:16px;background:rgba(2,6,23,0.92);border:1px solid #10b981;border-radius:14px;padding:16px;}
    .score-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
    .score-badge{background:rgba(16,185,129,0.18);color:#34d399;padding:4px 12px;border-radius:999px;font-weight:800;font-size:14px;}
    .bar-bg{width:100%;height:8px;background:#1e293b;border-radius:99px;overflow:hidden;margin-bottom:12px;}
    .bar-fill{height:100%;background:linear-gradient(90deg,#38bdf8,#10b981);width:0%;transition:width 0.8s ease;}
    .steps-list{margin:10px 0 14px 18px;font-size:13.5px;color:#cbd5e1;}
    .card h3{font-size:15.5px;color:#f8fafc;margin-bottom:5px;}
    .card p,.vo-card p{font-size:13px;color:#94a3b8;}
    footer{text-align:center;color:#64748b;font-size:13px;margin-top:20px;}
    footer a{color:#60a5fa;text-decoration:none;}
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>
  <div class="container">
    <div class="logo-wrap"><img src="/logo.svg" alt="aIValue8 Corporation" /></div>
    <div class="pulse-bar"><span class="dot"></span> aIValue8 Autonomous OS Live &bull; Mark 4.0 C-Suite Active</div>
    <div class="hero-title"><span id="typedText" class="typed"></span><span class="cursor"></span></div>
    <p class="hero-sub">AI Agents, Virtual Office SaaS, Website/App Build, Virtual CA Prep, CRM &amp; B2B Growth — sab ek hi live ecosystem mein.</p>

    <div class="telemetry">
      <div class="t-card"><div id="statAgents" class="t-num">-</div><div class="t-lbl">Active AI Clones</div></div>
      <div class="t-card"><div id="statGov" class="t-num">-</div><div class="t-lbl">Indian Law Checks</div></div>
      <div class="t-card"><div id="statHealed" class="t-num">-</div><div class="t-lbl">Self-Healed Bugs</div></div>
      <div class="t-card"><div id="statOpps" class="t-num">-</div><div class="t-lbl">Opportunities Found</div></div>
    </div>

    <div class="glass-box">
      <div class="box-head"><h2>⚙️ Live 7-Step Autonomous C-Suite Engine</h2><button class="sim-btn" onclick="runPipelineDemo()">▶ Watch Live Flow</button></div>
      <div class="pipeline">
        <div id="n0" class="node"><span class="ico">🌍</span><div class="n-title">1. CSO Hunt</div><div class="n-sub">4x Industry Scan</div></div>
        <div id="n1" class="node"><span class="ico">🧬</span><div class="n-title">2. Anti-Dup</div><div class="n-sub">SHA-256 Shield</div></div>
        <div id="n2" class="node"><span class="ico">⚖️</span><div class="n-title">3. Audit Guard</div><div class="n-sub">DPDP &amp; Ethics</div></div>
        <div id="n3" class="node"><span class="ico">👔</span><div class="n-title">4. COO Clones</div><div class="n-sub">Dept &amp; Outreach</div></div>
        <div id="n4" class="node"><span class="ico">🎬</span><div class="n-title">5. Media Reels</div><div class="n-sub">Auto Voice+IG</div></div>
        <div id="n5" class="node"><span class="ico">💹</span><div class="n-title">6. CFO / vCA</div><div class="n-sub">UPI &amp; Tax Prep</div></div>
        <div id="n6" class="node"><span class="ico">🛡️</span><div class="n-title">7. Self-Heal</div><div class="n-sub">24/7 Sentinel</div></div>
      </div>
      <div id="pipeLog" class="pipe-log">&gt; C-Suite Auto-Pilot Active... Click "Watch Live Flow" ya neeche Free AI test karein.</div>
    </div>

    <div class="glass-box">
      <div class="box-head"><h2>🏢 Digital Virtual Office &amp; SaaS Plans</h2><span style="font-size:12px;color:#94a3b8;">Online Workplace Software</span></div>
      <div class="vo-grid">
        <div class="vo-card">
          <h3>Starter Desk</h3>
          <div class="vo-price">₹199<span style="font-size:12px;color:#94a3b8;">/mo</span></div>
          <p>GPS Attendance, Task Board, Team Chat &amp; Basic CRM for small teams.</p>
          <button class="btn-outline" onclick="pickPlan('Virtual Office Starter Desk (Rs 199/mo)')">Select Starter</button>
        </div>
        <div class="vo-card">
          <h3>Growth Office</h3>
          <div class="vo-price">₹499<span style="font-size:12px;color:#94a3b8;">/mo</span></div>
          <p>Full CRM, WhatsApp Alerts, Virtual CA Expense Prep &amp; Team Reports.</p>
          <button class="btn-outline" onclick="pickPlan('Virtual Office Growth (Rs 499/mo)')">Select Growth</button>
        </div>
        <div class="vo-card">
          <h3>Enterprise + AI</h3>
          <div class="vo-price">₹999<span style="font-size:12px;color:#94a3b8;">/mo</span></div>
          <p>Dedicated AI Agents, Meeting Rooms, Custom Workflow &amp; Priority Support.</p>
          <button class="btn-outline" onclick="pickPlan('Virtual Office Enterprise AI (Rs 999/mo)')">Select Enterprise</button>
        </div>
      </div>
      <small style="color:#64748b;font-size:11.5px;">Note: Ye Digital Workplace Management software hai; GST/MCA registration ke liye physical address provide nahi karta.</small>
    </div>

    <div class="glass-box">
      <div class="box-head"><h2>🎬 Live AI Media &amp; Content Studio</h2><span style="font-size:12px;color:#34d399;">Auto-Generated Reels</span></div>
      <div id="mediaShowcase" class="media-grid"><div class="media-card">Loading live AI campaigns...</div></div>
    </div>

    <div class="glass-box">
      <h2>⚡ Live AI Business &amp; Tech Evaluator (Free Demo)</h2>
      <div class="chips">
        <span class="chip" onclick="fillDemo('Mujhe apne business ke liye website, app aur WhatsApp CRM automation chahiye.')">💻 Web/App + CRM</span>
        <span class="chip" onclick="fillDemo('Mujhe apni team ke liye Digital Virtual Office software aur GPS attendance chahiye.')">🏢 Virtual Office</span>
        <span class="chip" onclick="fillDemo('Mujhe Virtual CA bill tracking, GST prep aur B2B purchase-sell growth automate karna hai.')">💹 vCA &amp; Trade</span>
      </div>
      <textarea id="ideaInput" rows="2" placeholder="Apna business idea, website/app need ya trading requirement likhein..."></textarea>
      <button id="evalBtn" class="btn-glow" onclick="runEvaluator()">⚡ Evaluate With aIValue8 AI</button>
      <div id="evalErr" style="color:#f87171;font-size:13px;margin-top:8px;"></div>
      <div id="aiResult" class="ai-result">
        <div class="score-row"><strong id="resCategory" style="color:#38bdf8;font-size:14px;">AI Strategy</strong><span id="resScore" class="score-badge">90/100</span></div>
        <div class="bar-bg"><div id="scoreBar" class="bar-fill"></div></div>
        <p id="resSummary" style="font-size:14px;color:#f8fafc;margin-bottom:8px;"></p>
        <ul id="resSteps" class="steps-list"></ul>
        <div style="font-size:12px;color:#94a3b8;margin-bottom:10px;">⏱️ Build Time: <strong id="resTime" style="color:#34d399;"></strong></div>
        <button class="btn-outline" onclick="sendPlanToForm()">🚀 Is Plan Ko Execute Karwayein (Connect Now)</button>
      </div>
    </div>

    <div class="grid">
      <div class="card"><h3>🤖 Autonomous AI Clones</h3><p>COO, CFO, CSO aur Marketing Executive clones 24/7 active.</p></div>
      <div class="card"><h3>💻 Website &amp; App Build</h3><p>High-speed web platforms, SaaS dashboards &amp; Android apps.</p></div>
      <div class="card"><h3>💹 Virtual CA (vCA) Assistant</h3><p>Smart GST/ledger data prep aur registered CA ko scheduled reports.</p></div>
      <div class="card"><h3>📊 Multi-Channel CRM</h3><p>Email to WhatsApp fallback, Hot/Warm/Cold follow-ups &amp; deals.</p></div>
      <div class="card"><h3>🤝 Purchase &amp; Sell Support</h3><p>Verified B2B buyer-seller matching aur Job/Employer synergy.</p></div>
      <div class="card"><h3>⚖️ Indian Governance &amp; Audit</h3><p>DPDP Act 2023, RBI &amp; ASCI compliant ethical AI guardrails.</p></div>
    </div>

    <div class="glass-box" id="connectBox" style="border-color:#1e293b;">
      <h2 style="margin-bottom:8px;">📩 Start Your Project / Virtual Office Inquiry</h2>
      <form id="inquiryForm">
        <input type="text" id="name" placeholder="Aapka Naam / Company Name" required />
        <input type="text" id="contact" placeholder="Email ya WhatsApp Number" required />
        <select id="lead_type">
          <option value="BUYER">Product / Service Chahiye (AI, Web/App, Virtual Office)</option>
          <option value="SELLER">Main Seller / Supplier hoon (Purchase-Sell Support)</option>
          <option value="EMPLOYER">Employer / Hiring &amp; Team Automation</option>
          <option value="PARTNER">Business Growth &amp; Partnership</option>
        </select>
        <textarea id="requirement" rows="3" placeholder="Aapki requirement likhein..." required></textarea>
        <button type="submit" id="submitBtn" class="btn-glow">Submit Inquiry to aIValue8</button>
      </form>
      <div id="msg" style="margin-top:12px;font-size:14px;font-weight:600;"></div>
    </div>
    <footer><strong>aIValue8 Corporation (Sarahics)</strong> &bull; <a href="/panel">Owner Control Room</a></footer>
  </div>

  <div style="position:fixed;bottom:20px;right:20px;display:flex;flex-direction:column;gap:10px;z-index:9999;">
    <a href="https://t.me/aivalue8_rayan_bot"
       target="_blank"
       style="background:#0088cc;color:#fff;padding:10px 16px;border-radius:50px;font-family:sans-serif;font-size:13px;font-weight:bold;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.25);display:flex;align-items:center;gap:6px;">
       <span>✈️</span> Telegram Support
    </a>
    <a href="https://wa.me/__WA_NUM__?text=%5BGENERAL%5D%20Hi%20Sarahics%20Team%2C%20mujhe%20jankari%20chahiye"
       target="_blank"
       style="background:#25D366;color:#fff;padding:10px 16px;border-radius:50px;font-family:sans-serif;font-size:13px;font-weight:bold;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.25);display:flex;align-items:center;gap:6px;">
       <span>💬</span> WhatsApp Support
    </a>
  </div>

  <script>
    const canvas=document.getElementById('aiCanvas'),ctx=canvas.getContext('2d');let pts=[];
    function rsz(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}window.addEventListener('resize',rsz);rsz();
    for(let i=0;i<32;i++)pts.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-.5)*.6,vy:(Math.random()-.5)*.6});
    function anim(){ctx.clearRect(0,0,canvas.width,canvas.height);for(let i=0;i<pts.length;i++){let p=pts[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>canvas.width)p.vx*=-1;if(p.y<0||p.y>canvas.height)p.vy*=-1;ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(p.x,p.y,1.8,0,Math.PI*2);ctx.fill();for(let j=i+1;j<pts.length;j++){let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);if(d<125){ctx.strokeStyle=`rgba(52,211,153,${1-d/125})`;ctx.lineWidth=.6;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p2.x,p2.y);ctx.stroke();}}}requestAnimationFrame(anim);}anim();
    const phrases=["We Build AI & Automation.","We Rent Digital Virtual Offices.","We Build Websites & Apps.","We Power Purchase & Sell Growth."];let pI=0,cI=0,dl=false;
    function typ(){const c=phrases[pI],e=document.getElementById('typedText');if(!dl){e.textContent=c.slice(0,++cI);if(cI===c.length){dl=true;setTimeout(typ,1500);return;}}else{e.textContent=c.slice(0,--cI);if(cI===0){dl=false;pI=(pI+1)%phrases.length;}}setTimeout(typ,dl?35:65);}typ();
    async function loadTelemetry(){try{const r=await fetch('/public/telemetry'),d=await r.json();document.getElementById('statAgents').textContent=d.active_agents??0;document.getElementById('statGov').textContent=d.governance_checks??0;document.getElementById('statHealed').textContent=d.healed_bugs??0;document.getElementById('statOpps').textContent=d.opportunities_found??0;}catch(e){}}loadTelemetry();
    async function loadShowcase(){try{const r=await fetch('/public/showcase'),d=await r.json(),el=document.getElementById('mediaShowcase');el.innerHTML='';const arr=d.campaigns||[];if(!arr.length){const c=document.createElement('div');c.className='media-card';c.textContent='AI Media Studio ready.';el.appendChild(c);return;}arr.forEach(m=>{const c=document.createElement('div');c.className='media-card';const tag=document.createElement('span');tag.className='m-tag';tag.textContent=m.platform||'Social AI';const h=document.createElement('h4');h.style.color='#f8fafc';h.style.marginBottom='6px';h.textContent=m.title;const hk=document.createElement('p');hk.style.fontSize='12.5px';hk.style.color='#34d399';hk.textContent='🔥 Hook: '+m.hook;const sc=document.createElement('p');sc.style.fontSize='12px';sc.style.color='#94a3b8';sc.style.marginTop='6px';sc.textContent=(m.script_body||'').slice(0,140)+'...';c.appendChild(tag);c.appendChild(h);c.appendChild(hk);c.appendChild(sc);el.appendChild(c);});}catch(e){}}loadShowcase();
    const logs=["> [CSO] 4x Multi-Industry & Job/Employer signal detected...","> [Shield] SHA-256 Anti-Duplication: Unique ✓","> [Audit] Indian Law & Guardrails: APPROVED ✓","> [COO] Marketing Exec & Sales Clones engaged...","> [Media] Auto Reels Video + Hashtags published ✓","> [CFO/vCA] Base pricing, UPI & Tax ledger updated ✓","> [Sentinel] 100% Self-Healed & Live! 🚀"];let pipeRun=false;
    function runPipelineDemo(){if(pipeRun)return;pipeRun=true;for(let i=0;i<7;i++)document.getElementById('n'+i).className='node';let s=0;const iv=setInterval(()=>{if(s>0)document.getElementById('n'+(s-1)).className='node done';if(s<7){document.getElementById('n'+s).className='node active';document.getElementById('pipeLog').textContent=logs[s];s++;}else{clearInterval(iv);pipeRun=false;}},650);}
    setTimeout(runPipelineDemo,1200);
    function fillDemo(t){document.getElementById('ideaInput').value=t;}
    function pickPlan(p){document.getElementById('requirement').value='Interested in: '+p;document.getElementById('connectBox').scrollIntoView({behavior:'smooth'});document.getElementById('name').focus();}
    async function runEvaluator(){const idea=document.getElementById('ideaInput').value.trim(),err=document.getElementById('evalErr'),btn=document.getElementById('evalBtn'),box=document.getElementById('aiResult');err.textContent='';if(idea.length<8){err.textContent='Kam se kam 8 letters likhein.';return;}btn.disabled=true;btn.textContent='🧠 AI Analyze Kar Raha Hai...';box.style.display='none';runPipelineDemo();try{const r=await fetch('/public/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({business_idea:idea})}),d=await r.json();if(!r.ok)err.textContent='⚠️ '+(d.detail||'Error');else{document.getElementById('resCategory').textContent=d.category||'AI Solution';const sc=Math.min(100,Math.max(50,parseInt(d.growth_score||88)));document.getElementById('resScore').textContent='Growth Score: '+sc+'/100';document.getElementById('resSummary').textContent=d.summary||'';document.getElementById('resTime').textContent=d.launch_time||'7-14 Days';const ul=document.getElementById('resSteps');ul.innerHTML='';(d.steps||[]).forEach(x=>{const li=document.createElement('li');li.textContent=x;ul.appendChild(li);});box.style.display='block';setTimeout(()=>{document.getElementById('scoreBar').style.width=sc+'%';},100);loadTelemetry();}}catch(e){err.textContent='❌ Server error.';}btn.disabled=false;btn.textContent='⚡ Evaluate With aIValue8 AI';}
    function sendPlanToForm(){document.getElementById('requirement').value=`[${document.getElementById('resCategory').textContent}] ${document.getElementById('ideaInput').value.trim()}`;document.getElementById('connectBox').scrollIntoView({behavior:'smooth'});document.getElementById('name').focus();}
    document.getElementById('inquiryForm').addEventListener('submit',async(e)=>{e.preventDefault();const btn=document.getElementById('submitBtn'),msg=document.getElementById('msg');btn.disabled=true;msg.style.color='#94a3b8';msg.textContent='CRM mein save ho raha hai...';runPipelineDemo();try{const r=await fetch('/public/inquiry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lead_name:document.getElementById('name').value,contact:document.getElementById('contact').value,lead_type:document.getElementById('lead_type').value,requirement:document.getElementById('requirement').value})}),d=await r.json();if(d.status==='saved'){msg.style.color='#34d399';msg.textContent='✅ Dhanyawad! Detail CRM mein save ho gayi hai.';e.target.reset();loadTelemetry();}else if(d.status==='duplicate_skipped'){msg.style.color='#fbbf24';msg.textContent='ℹ️ Detail pehle se registered hai.';}else{msg.style.color='#f87171';msg.textContent='⚠️ '+(d.reason||d.message||'Submit nahi ho saka.');}}catch(err){msg.style.color='#f87171';msg.textContent='❌ Network error.';}btn.disabled=false;});
  </script>
</body>
</html>""".replace("__WA_NUM__", WA_NUMBER)

OWNER_PANEL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 — Owner Control Room</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#020617;color:#e2e8f0;padding:16px;}
    .wrap{max-width:940px;margin:0 auto;}
    .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;}
    .brand{display:flex;align-items:center;gap:10px;}
    .brand img{width:34px;height:34px;border-radius:8px;}
    h1{font-size:21px;color:#38bdf8;}
    .box{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:14px;}
    .box h3{font-size:15.5px;margin-bottom:10px;color:#f8fafc;}
    input,textarea{width:100%;background:#020617;color:#fff;border:1px solid #334155;border-radius:8px;padding:10px;margin-bottom:10px;font-size:14px;}
    button{background:#2563eb;color:#fff;border:none;padding:9px 14px;border-radius:8px;font-weight:600;cursor:pointer;margin:0 6px 6px 0;font-size:13px;}
    button.green{background:#059669;} button.cyan{background:#0284c7;} button.purple{background:#7c3aed;} button.red{background:#dc2626;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;}
    .w-card{background:#020617;border:1px solid #1e293b;border-radius:10px;padding:12px;}
    .w-card .amt{font-size:20px;font-weight:800;color:#34d399;margin-top:4px;}
    .item{background:#020617;border:1px solid #1e293b;border-radius:8px;padding:10px;margin-top:8px;font-size:13px;word-break:break-word;}
    .hidden{display:none;}
    a{color:#38bdf8;font-size:13px;text-decoration:none;}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top"><div class="brand"><img src="/icon.svg" alt="icon" /><h1>aIValue8 Owner Room</h1></div><a href="/">← Public Page</a></div>
    <div id="authBox" class="box">
      <input type="password" id="adminKey" placeholder="Apna AIVALUE8_ADMIN_KEY daalein..." />
      <button onclick="loadDash()">Unlock Control Room</button>
      <div id="authErr" style="color:#f87171;margin-top:8px;font-size:13px;"></div>
    </div>
    <div id="dash" class="hidden">
      <div class="box">
        <h3>🤖 Master Auto-Pilot &amp; C-Suite Controls</h3>
        <button class="purple" onclick="runCmd('/autopilot/run','Running Full Daily Auto-Pilot...')">🤖 Run Full Auto-Pilot</button>
        <button class="purple" onclick="runCmd('/csuite/run','Running COO, CFO/vCA & CSO Board...')">🏛️ Run C-Suite Board</button>
        <button class="cyan" onclick="runCmd('/scan/4x','Running 4x Multi-Industry & Job Scan...')">🔄 4x Industry Scan</button>
        <button onclick="runCmd('/hunter/scan','Scanning opportunities...')">🌍 Opportunity Scan</button>
        <button class="green" onclick="runCmd('/hunter/daily-venture','Creating Daily Venture...')">💡 Daily Venture</button>
        <button class="cyan" onclick="runCmd('/trade/match','Matching Buyers & Sellers...')">🤝 Trade Match</button>
        <button onclick="runCmd('/outreach/run','Running Email/WA Closer...')">📧 Email/WA Closer</button>
        <button class="green" onclick="runCmd('/media/create','Generating Motion Reel Video...')">🎬 Create Motion Reel</button>
        <div id="cmdRes" class="item hidden"></div>
      </div>
      <div class="box"><h3>💰 Treasury &amp; Wallets</h3><div id="wGrid" class="grid"></div></div>
      <div class="box">
        <h3>🧬 Clone Agent Factory</h3>
        <input id="agName" placeholder="Agent Name (e.g. Marketing_Clone_02)" />
        <input id="agDept" placeholder="Department (e.g. Marketing, Sales, CFO)" />
        <textarea id="agRole" rows="2" placeholder="Role Prompt..."></textarea>
        <button class="purple" onclick="spawnAgent()">🧬 Spawn Clone Agent</button>
        <div id="agRes" class="item hidden"></div>
        <div id="agList"></div>
      </div>
      <div class="box">
        <h3>💳 Client Payment Links (UPI / Bank)</h3>
        <input id="invName" placeholder="Client Name" />
        <input id="invContact" placeholder="Client WhatsApp / Email" />
        <input id="invDesc" placeholder="Service / Virtual Office Plan" />
        <input id="invAmt" type="number" placeholder="Amount in ₹" />
        <button class="green" onclick="makeInvoice()">Create Payment Link</button>
        <div id="invRes" class="item hidden"></div>
        <div id="invList"></div>
      </div>
      <div class="box">
        <h3>🧠 Talk to aIValue8 CEO</h3>
        <textarea id="ceoQ" rows="2" placeholder="CEO se koi sawal ya command poochhein..."></textarea>
        <button onclick="askCeo()">Send to CEO</button>
        <div id="ceoA" class="item hidden"></div>
      </div>
      <div class="box"><h3>🎬 Media Campaigns</h3><div id="mediaList"></div></div>
      <div class="box"><h3>🌍 Opportunities &amp; Daily Ventures</h3><div id="oppList"></div></div>
      <div class="box"><h3>🤝 Trade Matches</h3><div id="matchList"></div></div>
      <div class="box"><h3>📋 Recent CRM Leads</h3><div id="leadList"></div></div>
      <div class="box"><h3>📱 Phone Vision Evaluations</h3><div id="visList"></div></div>
      <div class="box"><h3>🛡️ Sentinel Self-Healing Logs</h3><div id="logList"></div></div>
    </div>
  </div>
  <script>
    let key=sessionStorage.getItem('av8_key')||'';if(key){document.getElementById('adminKey').value=key;loadDash();}
    async function loadDash(){
      const k=document.getElementById('adminKey').value.trim(),err=document.getElementById('authErr');err.textContent='';
      try{
        const r=await fetch('/dashboard',{headers:{'x-admin-key':k}});if(!r.ok){err.textContent='❌ Galat Admin Key!';return;}
        key=k;sessionStorage.setItem('av8_key',k);const d=await r.json();
        document.getElementById('authBox').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');
        const wg=document.getElementById('wGrid');wg.innerHTML='';
        (d.wallets||[]).forEach(w=>{const c=document.createElement('div');c.className='w-card';const t=document.createElement('div');t.style.fontSize='12px';t.style.color='#94a3b8';t.textContent=w.display_name+' ('+w.allocation_percent+'%)';const a=document.createElement('div');a.className='amt';a.textContent='₹'+w.balance_inr;c.appendChild(t);c.appendChild(a);wg.appendChild(c);});
        renderInvoices(d.recent_invoices||[]);
        renderList('mediaList',d.media_campaigns,m=>`[${m.platform}] ${m.title} | Hook: ${m.hook}`,'Abhi koi media campaign nahi.');
        renderList('oppList',d.recent_opportunities,o=>`[${o.score}/100 | ${o.category}] ${o.title} — ${o.action_plan}`,'Abhi koi opportunity scan nahi hui.');
        renderList('matchList',d.trade_matches,m=>`[${m.match_score}%] ${m.buyer_name} ↔️ ${m.seller_name} | ${m.item_summary}`,'Abhi koi match nahi.');
        renderList('agList',d.clone_agents,a=>`${a.agent_name} [${a.department}] — ${a.status} (Tasks: ${a.tasks_completed})`,'Koi clone agent nahi.');
        renderLeads(d.recent_leads||[]);
        renderList('visList',d.vision_evals,v=>`[${v.eval_type}] ${v.filename} (₹${v.estimated_value_inr}) — ${v.summary}`,'Abhi koi phone scan nahi.');
        renderList('logList',d.sentinel_logs,s=>`[${s.healed?'HEALED':'ALERT'}] ${s.module}: ${(s.error_text||'').slice(0,120)}`,'Koi error nahi.');
      }catch(e){err.textContent='❌ Server connect error.';}
    }
    function renderInvoices(arr){const el=document.getElementById('invList');el.innerHTML='';arr.forEach(inv=>{const d=document.createElement('div');d.className='item';const txt=document.createElement('span');txt.textContent=`[${inv.status}] ${inv.invoice_id} | ${inv.client_name} | ₹${inv.amount_inr} | UTR: ${inv.utr_number||'-'} `;d.appendChild(txt);const lnk=document.createElement('a');lnk.href='/pay/'+inv.invoice_id;lnk.target='_blank';lnk.textContent='[Open Link] ';d.appendChild(lnk);if(inv.status!=='PAID'){const b=document.createElement('button');b.className='green';b.style.padding='4px 10px';b.textContent='✅ Accept';b.onclick=async()=>{await fetch('/invoices/'+inv.invoice_id+'/approve',{method:'POST',headers:{'x-admin-key':key}});loadDash();};d.appendChild(b);const rb=document.createElement('button');rb.className='red';rb.style.padding='4px 10px';rb.textContent='❌ Reject';rb.onclick=async()=>{const rsn=prompt('Rejection ka reason likhein:');if(!rsn)return;await fetch('/invoices/'+inv.invoice_id+'/reject',{method:'POST',headers:{'Content-Type':'application/json','x-admin-key':key},body:JSON.stringify({reason:rsn})});loadDash();};d.appendChild(rb);}el.appendChild(d);});}
    function renderLeads(arr){const el=document.getElementById('leadList');el.innerHTML='';if(!arr.length){const d=document.createElement('div');d.className='item';d.textContent='Abhi koi lead nahi.';el.appendChild(d);return;}arr.forEach(l=>{const d=document.createElement('div');d.className='item';const s=document.createElement('span');s.textContent=`[${l.lead_type||''}|${l.temperature}] ${l.lead_name} (${l.contact}) — ${l.requirement} `;d.appendChild(s);const dig=(l.contact||'').replace(/\\D/g,'');if(dig.length>=10){const num=dig.length===10?'91'+dig:dig;const a=document.createElement('a');a.href=`https://wa.me/${num}?text=${encodeURIComponent('Namaste '+l.lead_name+', Sarahics aIValue8 se sampark kar rahe hain.')}`;a.target='_blank';a.textContent='[💬 WhatsApp]';d.appendChild(a);}el.appendChild(d);});}
    function renderList(id,arr,fmt,empty){const el=document.getElementById(id);el.innerHTML='';if(!arr||!arr.length){const d=document.createElement('div');d.className='item';d.textContent=empty;el.appendChild(d);return;}arr.forEach(x=>{const d=document.createElement('div');d.className='item';d.textContent=fmt(x);el.appendChild(d);});}
    async function runCmd(ep,wait){const b=document.getElementById('cmdRes');b.classList.remove('hidden');b.textContent=wait;const r=await fetch(ep,{method:'POST',headers:{'x-admin-key':key}});b.textContent=JSON.stringify(await r.json(),null,2);loadDash();}
    async function spawnAgent(){const b=document.getElementById('agRes');b.classList.remove('hidden');b.textContent='Spawning...';const r=await fetch('/agent/spawn',{method:'POST',headers:{'Content-Type':'application/json','x-admin-key':key},body:JSON.stringify({agent_name:document.getElementById('agName').value,department:document.getElementById('agDept').value,role_prompt:document.getElementById('agRole').value})});b.textContent=JSON.stringify(await r.json(),null,2);loadDash();}
    async function makeInvoice(){const b=document.getElementById('invRes');b.classList.remove('hidden');b.textContent='Creating link...';const r=await fetch('/invoices/create',{method:'POST',headers:{'Content-Type':'application/json','x-admin-key':key},body:JSON.stringify({client_name:document.getElementById('invName').value,client_contact:document.getElementById('invContact').value,description:document.getElementById('invDesc').value,amount_inr:parseFloat(document.getElementById('invAmt').value)})});const d=await r.json();b.textContent=d.pay_path?`✅ Link Ready: ${location.origin}${d.pay_path}`:JSON.stringify(d);loadDash();}
    async function askCeo(){const q=document.getElementById('ceoQ').value.trim();if(!q)return;const b=document.getElementById('ceoA');b.classList.remove('hidden');b.textContent='Soch raha hai...';const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_message:q,source:'panel'})});const d=await r.json();b.textContent=d.reply||d.detail||'Error';}
  </script>
</body>
</html>"""
