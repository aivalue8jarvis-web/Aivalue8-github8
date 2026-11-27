import os

_raw_wa = os.getenv("WHATSAPP_SUPPORT_NUMBER", "").strip()
_digits = "".join(c for c in _raw_wa if c.isdigit())
if len(_digits) == 10:
    _digits = "91" + _digits
WA_NUMBER = _digits if len(_digits) >= 10 else "91NAYA_NUMBER"

_DOCK_HTML = f"""  <div style="position:fixed;bottom:18px;right:18px;display:flex;flex-direction:column;gap:8px;z-index:9999;">
    <a href="https://t.me/aivalue8_rayan_bot" target="_blank" style="background:#0088cc;color:#fff;padding:9px 15px;border-radius:50px;font-family:sans-serif;font-size:13px;font-weight:bold;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.3);">✈️ Telegram Support</a>
    <a href="https://wa.me/{WA_NUMBER}?text=%5BGENERAL%5D%20Hi%20Sarahics%20Team%2C%20mujhe%20jankari%20chahiye" target="_blank" style="background:#25D366;color:#fff;padding:9px 15px;border-radius:50px;font-family:sans-serif;font-size:13px;font-weight:bold;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.3);">💬 WhatsApp Support</a>
  </div>"""

PUBLIC_HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Corporation — Sovereign Enterprise AI &amp; Automation OS</title>
  <meta name="description" content="Elite high-ticket B2B solutions, Hospital NABH systems, institutional trading tech, and sovereign AI enterprise ERP." />
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#030712;color:#e2e8f0;line-height:1.6;overflow-x:hidden;position:relative;}
    #aiCanvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.55;}
    .container{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:20px 16px 95px;}
    .logo-wrap{margin-bottom:16px;}
    .logo-wrap img{width:100%;max-width:630px;height:auto;display:block;border-radius:18px;border:1px solid rgba(56,189,248,0.25);box-shadow:0 0 35px rgba(37,99,235,0.2);}
    .ticker-bar{background:rgba(16,185,129,0.12);border:1px solid rgba(52,211,153,0.35);color:#34d399;padding:9px 14px;border-radius:12px;font-size:12.5px;font-weight:600;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
    .dot{width:8px;height:8px;background:#10b981;border-radius:50%;animation:pulse 1.5s infinite;flex-shrink:0;}
    @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,0.8);}70%{box-shadow:0 0 0 10px rgba(16,185,129,0);}100%{box-shadow:0 0 0 0 rgba(16,185,129,0);}}
    .hero-title{font-size:26px;font-weight:800;color:#f8fafc;margin-bottom:8px;min-height:38px;}
    .typed{background:linear-gradient(90deg,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .cursor{display:inline-block;width:3px;height:24px;background:#34d399;vertical-align:middle;animation:blink 0.8s infinite;margin-left:3px;}
    @keyframes blink{50%{opacity:0;}}
    .hero-sub{color:#94a3b8;font-size:14.5px;margin-bottom:18px;}
    .telemetry{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:10px;margin:16px 0 20px;}
    .t-card{background:rgba(15,23,42,0.82);border:1px solid #1e293b;border-radius:12px;padding:12px;text-align:center;}
    .t-num{font-size:20px;font-weight:800;color:#38bdf8;}
    .t-lbl{font-size:11.5px;color:#94a3b8;margin-top:2px;}
    .glass-box{background:rgba(15,23,42,0.78);backdrop-filter:blur(14px);border:1px solid rgba(56,189,248,0.3);border-radius:18px;padding:18px;margin-bottom:20px;}
    .box-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:14px;}
    .box-head h2{font-size:18px;color:#f8fafc;}
    .sim-btn{background:rgba(56,189,248,0.15);border:1px solid #38bdf8;color:#38bdf8;padding:6px 14px;border-radius:999px;font-size:12.5px;font-weight:700;cursor:pointer;}
    .pipeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:12px;}
    .node{background:#020617;border:1px solid #1e293b;border-radius:12px;padding:10px 6px;text-align:center;transition:0.35s;}
    .node .ico{font-size:18px;display:block;margin-bottom:3px;}
    .node .n-title{font-size:11.5px;font-weight:700;color:#cbd5e1;}
    .node .n-sub{font-size:10px;color:#64748b;}
    .node.active{border-color:#10b981;background:rgba(16,185,129,0.14);transform:translateY(-3px);}
    .node.done{border-color:#38bdf8;}
    .pipe-log{background:#020617;border:1px solid #1e293b;border-radius:10px;padding:10px;font-family:monospace;font-size:12px;color:#34d399;min-height:38px;}
    .grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:15px;margin-bottom:16px;}
    .card{background:rgba(2,6,23,0.92);border:1px solid #1e293b;border-radius:16px;padding:20px;display:flex;flex-direction:column;justify-content:space-between;}
    .price{font-size:24px;font-weight:900;color:#34d399;margin:8px 0;}
    .chips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 12px;}
    .chip{background:rgba(30,41,59,0.9);border:1px solid #334155;color:#cbd5e1;padding:6px 12px;border-radius:999px;font-size:12px;cursor:pointer;}
    input,select,textarea{width:100%;background:rgba(2,6,23,0.9);color:#f8fafc;border:1px solid #334155;border-radius:10px;padding:12px;margin-bottom:12px;font-size:14px;outline:none;}
    .btn-glow{width:100%;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:13px;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;}
    .btn-outline{width:100%;background:transparent;border:1px solid #38bdf8;color:#38bdf8;padding:9px;border-radius:8px;font-weight:700;cursor:pointer;margin-top:8px;}
    .ai-result{display:none;margin-top:14px;background:rgba(2,6,23,0.92);border:1px solid #10b981;border-radius:14px;padding:14px;}
    .media-grid,.vo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:16px;}
    .media-card,.vo-card{background:rgba(2,6,23,0.88);border:1px solid #1e293b;border-radius:14px;padding:15px;}
    .m-tag{display:inline-block;background:rgba(56,189,248,0.15);color:#38bdf8;font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;margin-bottom:6px;}
    footer{text-align:center;color:#64748b;font-size:13px;margin-top:24px;}
    footer a{color:#60a5fa;text-decoration:none;margin:0 4px;}
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>
  <div class="container">
    <div class="logo-wrap"><img src="/logo.svg" alt="aIValue8 Corporation" /></div>
    <div class="ticker-bar"><div class="dot"></div><div id="tickerText">🟢 Sovereign Enterprise Core Online &bull; Pure B2B Contracts Only</div></div>
    <div class="hero-title"><span id="typedText" class="typed"></span><span class="cursor"></span></div>
    <p class="hero-sub">Elite autonomous enterprise architecture, hospital NABH compliance systems, institutional trading tech, and sovereign AI ERP.</p>

    <div class="telemetry">
      <div class="t-card"><div id="statViewsToday" class="t-num">-</div><div class="t-lbl">Views (Today / Yest)</div></div>
      <div class="t-card"><div id="statServToday" class="t-num">-</div><div class="t-lbl">Contracts (Today / Yest)</div></div>
      <div class="t-card"><div id="statClients" class="t-num">-</div><div class="t-lbl">Enterprise Clients</div></div>
      <div class="t-card"><div id="statAgents" class="t-num">-</div><div class="t-lbl">Active Clones</div></div>
    </div>

    <!-- SOVEREIGN SOLUTIONS SHOWCASE (PURE HIGH-TICKET) -->
    <div class="glass-box">
      <div class="box-head"><h2>🏛️ Sovereign Enterprise &amp; High-Ticket Solutions</h2><span style="font-size:12px;color:#34d399;">Pure B2B Contracts Only</span></div>
      <div class="grid3">
        <div class="card">
          <div>
            <span style="background:rgba(56,189,248,0.15);color:#38bdf8;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">HEALTHCARE TECH</span>
            <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">Hospital NABH &amp; HMS Systems</h3>
            <div class="price">₹1L - ₹5L+</div>
            <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">Unified hospital management software &amp; digital NABH audit compliance automation for multi-facility clusters.</p>
          </div>
          <button class="btn-glow" onclick="requestProposal('Hospital NABH & HMS Enterprise Contract', 100000)">Request Proposal</button>
        </div>

        <div class="card">
          <div>
            <span style="background:rgba(16,185,129,0.15);color:#34d399;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">FINTECH INFRA</span>
            <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">Institutional Trading Tech</h3>
            <div class="price">₹2L - ₹10L+</div>
            <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">Custom algorithmic backtesters, risk engines, and sovereign trading infrastructure for funds &amp; institutes.</p>
          </div>
          <button class="btn-glow" onclick="requestProposal('Institutional Trading Tech Infrastructure', 200000)">Request Proposal</button>
        </div>

        <div class="card">
          <div>
            <span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">ENTERPRISE ERP</span>
            <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">Custom Sovereign AI ERP</h3>
            <div class="price">₹1.5L+</div>
            <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">Multi-department generative enterprise workspace tailored for global corporations with zero leakage.</p>
          </div>
          <button class="btn-glow" onclick="requestProposal('Custom Sovereign AI Enterprise ERP', 150000)">Request Proposal</button>
        </div>
      </div>

      <!-- PROPOSAL REQUEST BOX -->
      <div id="proposalBox" style="display:none;background:#020617;border:1px solid #10b981;border-radius:14px;padding:16px;margin-top:14px;">
        <h3 style="margin-bottom:8px;color:#34d399;">📋 Request Enterprise Proposal</h3>
        <form id="propForm">
          <input id="prName" placeholder="Enterprise / Hospital / Fund Name" required />
          <input id="prContact" placeholder="Official Email or WhatsApp Number" required />
          <input id="prDesc" readonly />
          <input id="prVal" type="number" readonly />
          <button type="submit" id="prBtn" class="btn-glow">Dispatch Sovereign Proposal</button>
        </form>
        <div id="prMsg" style="margin-top:8px;font-size:13.5px;"></div>
      </div>
    </div>

    <!-- HOLDING ECOSYSTEM PRODUCTIONS -->
    <div class="glass-box">
      <div class="box-head"><h2>🏛️ aIValue8 Holding Ecosystem &amp; Productions</h2><span style="font-size:12px;color:#34d399;">In-House Platforms</span></div>
      <div class="media-grid">
        <div class="media-card"><span class="m-tag">FINTECH</span><h4 style="color:#f8fafc;margin-bottom:4px;">Anas Trading Institute</h4><p style="font-size:12.5px;color:#94a3b8;margin-bottom:8px;">Financial market education &amp; algorithmic tech.</p><a href="https://anas.sarahics.in" target="_blank" style="color:#38bdf8;font-size:12px;">Visit Anas ↗</a></div>
        <div class="media-card"><span class="m-tag">EMOTIONAL AI</span><h4 style="color:#f8fafc;margin-bottom:4px;">Saifu Virtual Family</h4><p style="font-size:12.5px;color:#94a3b8;margin-bottom:8px;">24/7 empathetic AI companion &amp; support.</p><a href="https://saifu.sarahics.in" target="_blank" style="color:#38bdf8;font-size:12px;">Visit Saifu ↗</a></div>
        <div class="media-card"><span class="m-tag">SECURITY</span><h4 style="color:#f8fafc;margin-bottom:4px;">Kavach Data Shield</h4><p style="font-size:12.5px;color:#94a3b8;margin-bottom:8px;">Sovereign encryption &amp; privacy vault.</p><a href="https://kavach.sarahics.in" target="_blank" style="color:#38bdf8;font-size:12px;">Visit Kavach ↗</a></div>
        <div class="media-card"><span class="m-tag">AUTOMATION</span><h4 style="color:#f8fafc;margin-bottom:4px;">Miracle Automation</h4><p style="font-size:12.5px;color:#94a3b8;margin-bottom:8px;">High-speed workflow synchronizer.</p><a href="https://miracle.sarahics.in" target="_blank" style="color:#38bdf8;font-size:12px;">Visit Miracle ↗</a></div>
      </div>
    </div>

    <!-- LIVE EVALUATOR -->
    <div class="glass-box">
      <h2>⚡ Sovereign Enterprise Architect Evaluator</h2>
      <div class="chips">
        <span class="chip" onclick="fillDemo('We need a multi-facility hospital NABH compliance and HMS integration in Bhopal.')">🏥 Hospital NABH &amp; HMS</span>
        <span class="chip" onclick="fillDemo('We require a custom algorithmic trading infrastructure and risk management backend.')">📈 Trading Tech</span>
        <span class="chip" onclick="fillDemo('We need a secure multi-department sovereign AI ERP for our global corporation.')">🌐 Sovereign AI ERP</span>
      </div>
      <textarea id="ideaInput" rows="2" placeholder="Describe your enterprise scale requirement..."></textarea>
      <button id="evalBtn" class="btn-glow" onclick="runEvaluator()">⚡ Evaluate Enterprise Architecture</button>
      <div id="evalErr" style="color:#f87171;font-size:13px;margin-top:8px;"></div>
      <div id="aiResult" class="ai-result">
        <strong id="resCategory" style="color:#38bdf8;"></strong> &bull; <strong id="resScore" style="color:#34d399;"></strong>
        <p id="resSummary" style="font-size:14px;margin:8px 0;"></p>
        <ul id="resSteps" style="margin-left:18px;font-size:13px;color:#cbd5e1;"></ul>
      </div>
    </div>

    <footer>
      <strong>aIValue8 Corporation (Sarahics)</strong> &bull; 
      <a href="/mission">Mission</a> &bull; 
      <a href="/family">Virtual Family</a> &bull; 
      <a href="/results">Results</a> &bull; 
      <a href="/privacy">Privacy</a> &bull; 
      <a href="/terms">Terms</a> &bull; 
      <a href="/contact">Contact</a> &bull; 
      <a href="/panel">Owner Room</a>
    </footer>
  </div>
""" + _DOCK_HTML + """
  <script>
    const canvas=document.getElementById('aiCanvas'),ctx=canvas.getContext('2d');let pts=[];
    function rsz(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}window.addEventListener('resize',rsz);rsz();
    for(let i=0;i<30;i++)pts.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5});
    function anim(){ctx.clearRect(0,0,canvas.width,canvas.height);for(let i=0;i<pts.length;i++){let p=pts[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>canvas.width)p.vx*=-1;if(p.y<0||p.y>canvas.height)p.vy*=-1;ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(p.x,p.y,1.6,0,Math.PI*2);ctx.fill();for(let j=i+1;j<pts.length;j++){let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);if(d<120){ctx.strokeStyle=`rgba(52,211,153,${1-d/120})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p2.x,p2.y);ctx.stroke();}}}requestAnimationFrame(anim);}anim();
    const phrases=["Pure High-Ticket B2B Contracts.","Hospital NABH & HMS Systems.","Institutional Trading Technology.","Custom Sovereign AI ERP Solutions."];let pI=0,cI=0,dl=false;
    function typ(){const c=phrases[pI],e=document.getElementById('typedText');if(!dl){e.textContent=c.slice(0,++cI);if(cI===c.length){dl=true;setTimeout(typ,1500);return;}}else{e.textContent=c.slice(0,--cI);if(cI===0){dl=false;pI=(pI+1)%phrases.length;}}setTimeout(typ,dl?35:65);}typ();
    async function loadStats(){try{const r=await fetch('/public/analytics'),d=await r.json();document.getElementById('statViewsToday').textContent=(d.views_today??0)+' / '+(d.views_yesterday??0);document.getElementById('statServToday').textContent=(d.services_today??0)+' / '+(d.services_yesterday??0);document.getElementById('statClients').textContent=d.total_clients??0;const r2=await fetch('/public/telemetry'),t=await r2.json();document.getElementById('statAgents').textContent=t.active_agents??0;}catch(e){}}loadStats();
    
    function requestProposal(desc,val){document.getElementById('prDesc').value=desc;document.getElementById('prVal').value=val;const b=document.getElementById('proposalBox');b.style.display='block';b.scrollIntoView({behavior:'smooth'});document.getElementById('prName').focus();}
    document.getElementById('propForm').addEventListener('submit',async(e)=>{e.preventDefault();const b=document.getElementById('prBtn'),m=document.getElementById('prMsg');b.disabled=true;m.textContent='Dispatching Sovereign Proposal...';try{const r=await fetch('/sovereign/proposal',{method:'POST',headers:{'Content-Type':'application/json','x-admin-key':'646699'},body:JSON.stringify({client_name:document.getElementById('prName').value,enterprise_need:document.getElementById('prDesc').value})});const d=await r.json();if(d.status==='proposal_ready'){m.style.color='#34d399';m.innerHTML=`✅ Proposal Dispatched Successfully! Value: ₹${d.proposal.estimated_value_inr.toLocaleString()}`;e.target.reset();}else{m.style.color='#f87171';m.textContent='⚠️ '+(d.detail||'Error');}}catch(err){m.textContent='Network error';}b.disabled=false;});
    
    function fillDemo(t){document.getElementById('ideaInput').value=t;}
    async function runEvaluator(){const idea=document.getElementById('ideaInput').value.trim(),err=document.getElementById('evalErr'),btn=document.getElementById('evalBtn'),box=document.getElementById('aiResult');err.textContent='';if(idea.length<8){err.textContent='Min 8 letters.';return;}btn.disabled=true;btn.textContent='🧠 Architect analyzing...';box.style.display='none';try{const r=await fetch('/public/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({business_idea:idea})}),d=await r.json();if(!r.ok)err.textContent=d.detail||'Error';else{document.getElementById('resCategory').textContent=d.category||'Sovereign Architecture';document.getElementById('resScore').textContent='Score: '+(d.growth_score||95)+'/100';document.getElementById('resSummary').textContent=d.summary||'';const ul=document.getElementById('resSteps');ul.innerHTML='';(d.steps||[]).forEach(x=>{const li=document.createElement('li');li.textContent=x;ul.appendChild(li);});box.style.display='block';}}catch(e){err.textContent='Server error';}btn.disabled=false;btn.textContent='⚡ Evaluate Enterprise Architecture';}
  </script>
</body>
</html>"""
