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
  <title>aIValue8 Corporation — AI Micro-Store, Virtual Office &amp; Automation</title>
  <meta name="description" content="Deploy AI ATS resumes for ₹29, local shop mini-websites for ₹99, or virtual office software via UPI." />
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#030712;color:#e2e8f0;line-height:1.6;overflow-x:hidden;position:relative;}
    #aiCanvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.55;}
    .container{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:20px 16px 95px;}
    .logo-wrap{margin-bottom:14px;}
    .logo-wrap img{width:100%;max-width:630px;height:auto;display:block;border-radius:18px;border:1px solid rgba(56,189,248,0.25);box-shadow:0 0 35px rgba(37,99,235,0.2);}
    .ticker-bar{background:rgba(16,185,129,0.12);border:1px solid rgba(52,211,153,0.35);color:#34d399;padding:9px 14px;border-radius:12px;font-size:12.5px;font-weight:600;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
    .dot{width:8px;height:8px;background:#10b981;border-radius:50%;animation:pulse 1.5s infinite;flex-shrink:0;}
    @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,0.8);}70%{box-shadow:0 0 0 10px rgba(16,185,129,0);}100%{box-shadow:0 0 0 0 rgba(16,185,129,0);}}
    .hero-title{font-size:25px;font-weight:800;color:#f8fafc;margin-bottom:6px;min-height:36px;}
    .typed{background:linear-gradient(90deg,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .cursor{display:inline-block;width:3px;height:22px;background:#34d399;vertical-align:middle;animation:blink 0.8s infinite;margin-left:3px;}
    @keyframes blink{50%{opacity:0;}}
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
    .grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:12px;margin-bottom:14px;}
    .card{background:rgba(2,6,23,0.9);border:1px solid #1e293b;border-radius:14px;padding:16px;display:flex;flex-direction:column;justify-content:space-between;}
    .price{font-size:24px;font-weight:900;color:#34d399;margin:6px 0;}
    .chips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 12px;}
    .chip{background:rgba(30,41,59,0.9);border:1px solid #334155;color:#cbd5e1;padding:6px 12px;border-radius:999px;font-size:12px;cursor:pointer;}
    input,select,textarea{width:100%;background:rgba(2,6,23,0.9);color:#f8fafc;border:1px solid #334155;border-radius:10px;padding:12px;margin-bottom:12px;font-size:14px;outline:none;}
    .btn-glow{width:100%;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:12px;border-radius:10px;font-size:14.5px;font-weight:700;cursor:pointer;}
    .btn-glow:disabled{opacity:0.6;}
    .btn-outline{width:100%;background:transparent;border:1px solid #38bdf8;color:#38bdf8;padding:9px;border-radius:8px;font-weight:700;cursor:pointer;margin-top:8px;}
    .ai-result{display:none;margin-top:14px;background:rgba(2,6,23,0.92);border:1px solid #10b981;border-radius:14px;padding:14px;}
    footer{text-align:center;color:#64748b;font-size:13px;margin-top:20px;}
    footer a{color:#60a5fa;text-decoration:none;}
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>
  <div class="container">
    <div class="logo-wrap"><img src="/logo.svg" alt="aIValue8 Corporation" /></div>
    <div class="ticker-bar"><div class="dot"></div><div id="tickerText">🟢 aIValue8 Autonomous Core Online &bull; Zero Fake Data</div></div>
    <div class="hero-title"><span id="typedText" class="typed"></span><span class="cursor"></span></div>

    <div class="telemetry">
      <div class="t-card"><div id="statViewsToday" class="t-num">-</div><div class="t-lbl">Views (Today / Yest)</div></div>
      <div class="t-card"><div id="statServToday" class="t-num">-</div><div class="t-lbl">Services (Today / Yest)</div></div>
      <div class="t-card"><div id="statClients" class="t-num">-</div><div class="t-lbl">Total Clients</div></div>
      <div class="t-card"><div id="statAgents" class="t-num">-</div><div class="t-lbl">Active Clones</div></div>
    </div>

    <div class="glass-box">
      <div class="box-head"><h2>⚙️ Live 7-Step Autonomous C-Suite Engine</h2><button class="sim-btn" onclick="runPipelineDemo()">▶ Watch Live Flow</button></div>
      <div class="pipeline">
        <div id="n0" class="node"><span class="ico">🌍</span><div class="n-title">1. CSO Hunt</div><div class="n-sub">4x Scan</div></div>
        <div id="n1" class="node"><span class="ico">🧬</span><div class="n-title">2. Anti-Dup</div><div class="n-sub">SHA-256</div></div>
        <div id="n2" class="node"><span class="ico">⚖️</span><div class="n-title">3. Audit Guard</div><div class="n-sub">Indian Law</div></div>
        <div id="n3" class="node"><span class="ico">👔</span><div class="n-title">4. COO Clones</div><div class="n-sub">Dept &amp; Sales</div></div>
        <div id="n4" class="node"><span class="ico">🎬</span><div class="n-title">5. Media Reels</div><div class="n-sub">Auto Video</div></div>
        <div id="n5" class="node"><span class="ico">💹</span><div class="n-title">6. CFO / vCA</div><div class="n-sub">UPI &amp; Tax</div></div>
        <div id="n6" class="node"><span class="ico">🛡️</span><div class="n-title">7. Self-Heal</div><div class="n-sub">24/7 Sentinel</div></div>
      </div>
      <div id="pipeLog" class="pipe-log">&gt; C-Suite Auto-Pilot Ready...</div>
    </div>

    <div class="glass-box">
      <div class="box-head"><h2>🛒 Instant AI Micro-Store (Crowd Pricing)</h2><a href="/store" style="color:#38bdf8;font-size:13px;">Full Store Page →</a></div>
      <div class="grid3">
        <div class="card"><div><h3>📄 ATS Resume &amp; Cover</h3><div class="price">₹29</div><p style="font-size:13px;color:#94a3b8;">AI-optimized printable Resume + Cover Letter live page.</p></div><button class="btn-glow" style="margin-top:12px;" onclick="orderNow('ATS Resume & Cover Letter Kit', 29)">Buy Now (₹29)</button></div>
        <div class="card"><div><h3>🏪 Shop Mini-Website</h3><div class="price">₹99</div><p style="font-size:13px;color:#94a3b8;">Mobile website + WhatsApp Order button for shops &amp; clinics.</p></div><button class="btn-glow" style="margin-top:12px;" onclick="orderNow('Local Shop Mini-Website & QR Menu', 99)">Buy Now (₹99)</button></div>
        <div class="card"><div><h3>🏢 Virtual Office Desk</h3><div class="price">₹49<span style="font-size:12px;color:#94a3b8;">/mo</span></div><p style="font-size:13px;color:#94a3b8;">Digital Workplace software (Tasks, Attendance &amp; CRM).</p></div><button class="btn-glow" style="margin-top:12px;" onclick="orderNow('Virtual Office Starter Desk', 49)">Start Trial (₹49)</button></div>
      </div>
      <div id="quickPayBox" style="display:none;background:#020617;border:1px solid #10b981;border-radius:12px;padding:14px;">
        <h3 style="margin-bottom:8px;color:#34d399;">⚡ Instant UPI Checkout</h3>
        <form id="quickOrderForm">
          <input id="qoName" placeholder="Aapka Naam / Shop Name" required />
          <input id="qoContact" placeholder="Email ya WhatsApp Number (Delivery ke liye)" required />
          <input id="qoDesc" readonly />
          <input id="qoAmt" type="number" readonly />
          <button type="submit" id="qoBtn" class="btn-glow">Pay via UPI QR Now</button>
        </form>
        <div id="qoMsg" style="margin-top:8px;font-size:13.5px;"></div>
      </div>
    </div>

    <div class="glass-box">
      <h2>⚡ Live AI Business &amp; Tech Evaluator (Free Demo)</h2>
      <div class="chips">
        <span class="chip" onclick="fillDemo('Mujhe website, app aur WhatsApp CRM automation chahiye.')">💻 Web/App + CRM</span>
        <span class="chip" onclick="fillDemo('Mujhe apni team ke liye Digital Virtual Office software chahiye.')">🏢 Virtual Office</span>
        <span class="chip" onclick="fillDemo('Mujhe Virtual CA bill tracking aur B2B growth automate karna hai.')">💹 vCA &amp; Trade</span>
      </div>
      <textarea id="ideaInput" rows="2" placeholder="Apna business idea ya requirement likhein..."></textarea>
      <button id="evalBtn" class="btn-glow" onclick="runEvaluator()">⚡ Evaluate With aIValue8 AI</button>
      <div id="evalErr" style="color:#f87171;font-size:13px;margin-top:8px;"></div>
      <div id="aiResult" class="ai-result">
        <strong id="resCategory" style="color:#38bdf8;"></strong> — <strong id="resScore" style="color:#34d399;"></strong>
        <p id="resSummary" style="font-size:14px;margin:8px 0;"></p>
        <ul id="resSteps" style="margin-left:18px;font-size:13px;color:#cbd5e1;"></ul>
        <button class="btn-outline" onclick="sendPlanToForm()">🚀 Connect to Build This</button>
      </div>
    </div>

    <div class="glass-box" id="connectBox" style="border-color:#1e293b;">
      <h2 style="margin-bottom:8px;">📩 Custom Project / Business Inquiry</h2>
      <form id="inquiryForm">
        <input id="name" placeholder="Aapka Naam / Company Name" required />
        <input id="contact" placeholder="Email ya WhatsApp Number" required />
        <select id="lead_type"><option value="BUYER">Product / Service Chahiye</option><option value="SELLER">Seller / Supplier</option><option value="EMPLOYER">Employer / Hiring</option><option value="PARTNER">Partnership</option></select>
        <textarea id="requirement" rows="3" placeholder="Aapki requirement likhein..." required></textarea>
        <button type="submit" id="submitBtn" class="btn-glow">Submit Inquiry</button>
      </form>
      <div id="msg" style="margin-top:10px;font-size:14px;font-weight:600;"></div>
    </div>
    <footer><strong>aIValue8 Corporation (Sarahics)</strong> &bull; <a href="/store">Micro-Store</a> &bull; <a href="/panel">Owner Room</a></footer>
  </div>
""" + _DOCK_HTML + """
  <script>
    const canvas=document.getElementById('aiCanvas'),ctx=canvas.getContext('2d');let pts=[];
    function rsz(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}window.addEventListener('resize',rsz);rsz();
    for(let i=0;i<30;i++)pts.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5});
    function anim(){ctx.clearRect(0,0,canvas.width,canvas.height);for(let i=0;i<pts.length;i++){let p=pts[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>canvas.width)p.vx*=-1;if(p.y<0||p.y>canvas.height)p.vy*=-1;ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(p.x,p.y,1.6,0,Math.PI*2);ctx.fill();for(let j=i+1;j<pts.length;j++){let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);if(d<120){ctx.strokeStyle=`rgba(52,211,153,${1-d/120})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p2.x,p2.y);ctx.stroke();}}}requestAnimationFrame(anim);}anim();
    const phrases=["We Build AI & Automation.","Start at Just ₹29 via UPI.","We Rent Digital Virtual Offices.","We Scale Purchase & Sell Trade."];let pI=0,cI=0,dl=false;
    function typ(){const c=phrases[pI],e=document.getElementById('typedText');if(!dl){e.textContent=c.slice(0,++cI);if(cI===c.length){dl=true;setTimeout(typ,1500);return;}}else{e.textContent=c.slice(0,--cI);if(cI===0){dl=false;pI=(pI+1)%phrases.length;}}setTimeout(typ,dl?35:65);}typ();
    async function loadStats(){try{const r=await fetch('/public/analytics'),d=await r.json();document.getElementById('statViewsToday').textContent=(d.views_today??0)+' / '+(d.views_yesterday??0);document.getElementById('statServToday').textContent=(d.services_today??0)+' / '+(d.services_yesterday??0);document.getElementById('statClients').textContent=d.total_clients??0;const r2=await fetch('/public/telemetry'),t=await r2.json();document.getElementById('statAgents').textContent=t.active_agents??0;document.getElementById('tickerText').textContent=`🟢 Live Core Online • Views Today: ${d.views_today??0} • Active AI Clones: ${t.active_agents??0} • 100% Ethical & Real`;}catch(e){}}loadStats();
    const logs=["> [CSO] Multi-Industry scan...","> [Shield] Zero Duplicates ✓","> [Audit] Indian Law Approved ✓","> [COO] Clones active...","> [Media] Reels Studio ready ✓","> [CFO/vCA] UPI & Tax ready ✓","> [Sentinel] 100% Self-Healed 🚀"];let pRun=false;
    function runPipelineDemo(){if(pRun)return;pRun=true;for(let i=0;i<7;i++)document.getElementById('n'+i).className='node';let s=0;const iv=setInterval(()=>{if(s>0)document.getElementById('n'+(s-1)).className='node done';if(s<7){document.getElementById('n'+s).className='node active';document.getElementById('pipeLog').textContent=logs[s];s++;}else{clearInterval(iv);pRun=false;}},600);}setTimeout(runPipelineDemo,1000);
    function orderNow(desc,amt){document.getElementById('qoDesc').value=desc;document.getElementById('qoAmt').value=amt;const b=document.getElementById('quickPayBox');b.style.display='block';b.scrollIntoView({behavior:'smooth'});document.getElementById('qoName').focus();}
    document.getElementById('quickOrderForm').addEventListener('submit',async(e)=>{e.preventDefault();const b=document.getElementById('qoBtn'),m=document.getElementById('qoMsg');b.disabled=true;m.textContent='Creating UPI Link...';try{const r=await fetch('/public/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({client_name:document.getElementById('qoName').value,client_contact:document.getElementById('qoContact').value,description:document.getElementById('qoDesc').value,amount_inr:parseFloat(document.getElementById('qoAmt').value)})});const d=await r.json();if(d.pay_path){location.href=d.pay_path;}else{m.style.color='#f87171';m.textContent=d.detail||d.reason||'Error';}}catch(err){m.textContent='Network error';}b.disabled=false;});
    function fillDemo(t){document.getElementById('ideaInput').value=t;}
    async function runEvaluator(){const idea=document.getElementById('ideaInput').value.trim(),err=document.getElementById('evalErr'),btn=document.getElementById('evalBtn'),box=document.getElementById('aiResult');err.textContent='';if(idea.length<8){err.textContent='Min 8 letters likhein.';return;}btn.disabled=true;btn.textContent='🧠 Analyzing...';box.style.display='none';runPipelineDemo();try{const r=await fetch('/public/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({business_idea:idea})}),d=await r.json();if(!r.ok)err.textContent=d.detail||'Error';else{document.getElementById('resCategory').textContent=d.category||'AI Plan';document.getElementById('resScore').textContent='Score: '+(d.growth_score||88)+'/100';document.getElementById('resSummary').textContent=d.summary||'';const ul=document.getElementById('resSteps');ul.innerHTML='';(d.steps||[]).forEach(x=>{const li=document.createElement('li');li.textContent=x;ul.appendChild(li);});box.style.display='block';}}catch(e){err.textContent='Server error';}btn.disabled=false;btn.textContent='⚡ Evaluate With aIValue8 AI';}
    function sendPlanToForm(){document.getElementById('requirement').value=document.getElementById('ideaInput').value;document.getElementById('connectBox').scrollIntoView({behavior:'smooth'});}
    document.getElementById('inquiryForm').addEventListener('submit',async(e)=>{e.preventDefault();const b=document.getElementById('submitBtn'),m=document.getElementById('msg');b.disabled=true;m.textContent='Saving...';try{const r=await fetch('/public/inquiry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lead_name:document.getElementById('name').value,contact:document.getElementById('contact').value,lead_type:document.getElementById('lead_type').value,requirement:document.getElementById('requirement').value})}),d=await r.json();m.style.color=d.status==='saved'?'#34d399':'#fbbf24';m.textContent=d.status==='saved'?'✅ Saved to CRM!':'ℹ️ '+(d.message||d.reason);if(d.status==='saved')e.target.reset();}catch(err){m.textContent='Error';}b.disabled=false;});
  </script>
</body>
</html>"""

PUBLIC_STORE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Instant Micro-Store — ₹29 / ₹49 / ₹99</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif;}body{background:#030712;color:#e2e8f0;padding:18px 16px 90px;}.c{max-width:860px;margin:0 auto;}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:18px 0;}.card{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:18px;}.p{font-size:28px;font-weight:900;color:#34d399;margin:8px 0;}input{width:100%;background:#020617;color:#fff;border:1px solid #334155;border-radius:8px;padding:11px;margin-bottom:10px;}.btn{width:100%;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:12px;border-radius:8px;font-weight:700;cursor:pointer;}</style>
</head>
<body>
  <div class="c">
    <img src="/logo.svg" style="width:100%;max-width:560px;border-radius:14px;margin-bottom:14px;" alt="aIValue8" />
    <h1 style="color:#38bdf8;font-size:24px;">🛒 Instant AI Micro-Store (Pay via UPI)</h1>
    <div class="g">
      <div class="card"><h3>📄 ATS Resume &amp; Cover</h3><div class="p">₹29</div><p style="font-size:13px;color:#94a3b8;margin-bottom:12px;">Instant ATS-friendly printable Resume + Cover Letter.</p><button class="btn" onclick="pick('ATS Resume & Cover Letter Kit',29)">Buy ₹29</button></div>
      <div class="card"><h3>🏪 Shop Mini-Website</h3><div class="p">₹99</div><p style="font-size:13px;color:#94a3b8;margin-bottom:12px;">Live mobile website + WhatsApp Order button.</p><button class="btn" onclick="pick('Local Shop Mini-Website & QR Menu',99)">Buy ₹99</button></div>
      <div class="card"><h3>🏢 Virtual Office Desk</h3><div class="p">₹49/mo</div><p style="font-size:13px;color:#94a3b8;margin-bottom:12px;">Digital workplace software trial for small teams.</p><button class="btn" onclick="pick('Virtual Office Starter Desk',49)">Start ₹49</button></div>
    </div>
    <div class="card" id="chk">
      <h3 style="margin-bottom:10px;">⚡ Instant UPI Checkout</h3>
      <form id="sf">
        <input id="sn" placeholder="Aapka Naam / Shop Name" required />
        <input id="sc" placeholder="Email ya WhatsApp Number" required />
        <input id="sd" placeholder="Service Details (e.g. Python Dev Resume ya Royal Cafe)" required />
        <input id="sa" type="number" placeholder="Amount ₹ (Min 29)" required />
        <button type="submit" id="sb" class="btn">Generate UPI Payment Page</button>
      </form>
      <div id="sm" style="margin-top:10px;font-size:14px;"></div>
    </div>
    <div style="text-align:center;margin-top:16px;"><a href="/" style="color:#38bdf8;">← Back to Home</a></div>
  </div>
""" + _DOCK_HTML + """
  <script>
    function pick(d,a){document.getElementById('sd').value=d;document.getElementById('sa').value=a;document.getElementById('chk').scrollIntoView({behavior:'smooth'});document.getElementById('sn').focus();}
    document.getElementById('sf').addEventListener('submit',async(e)=>{e.preventDefault();const b=document.getElementById('sb'),m=document.getElementById('sm');b.disabled=true;m.textContent='Creating UPI Link...';try{const r=await fetch('/public/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({client_name:document.getElementById('sn').value,client_contact:document.getElementById('sc').value,description:document.getElementById('sd').value,amount_inr:parseFloat(document.getElementById('sa').value)})});const d=await r.json();if(d.pay_path){location.href=d.pay_path;}else{m.style.color='#f87171';m.textContent=d.detail||d.reason||'Error';}}catch(err){m.textContent='Network error';}b.disabled=false;});
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
  <style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif;}body{background:#020617;color:#e2e8f0;padding:16px;}.wrap{max-width:940px;margin:0 auto;}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;}.box{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:14px;}input,textarea{width:100%;background:#020617;color:#fff;border:1px solid #334155;border-radius:8px;padding:10px;margin-bottom:10px;}button{background:#2563eb;color:#fff;border:none;padding:9px 14px;border-radius:8px;font-weight:600;cursor:pointer;margin:0 6px 6px 0;font-size:13px;}button.green{background:#059669;}button.cyan{background:#0284c7;}button.purple{background:#7c3aed;}button.red{background:#dc2626;}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;}.w-card{background:#020617;border:1px solid #1e293b;border-radius:10px;padding:12px;}.amt{font-size:20px;font-weight:800;color:#34d399;margin-top:4px;}.item{background:#020617;border:1px solid #1e293b;border-radius:8px;padding:10px;margin-top:8px;font-size:13px;word-break:break-word;}.hidden{display:none;}a{color:#38bdf8;text-decoration:none;}</style>
</head>
<body>
  <div class="wrap">
    <div class="top"><h1 style="font-size:21px;color:#38bdf8;">👑 aIValue8 Owner Room</h1><a href="/">← Public Page</a></div>
    <div id="authBox" class="box"><input type="password" id="adminKey" placeholder="Apna AIVALUE8_ADMIN_KEY daalein..." /><button onclick="loadDash()">Unlock Control Room</button><div id="authErr" style="color:#f87171;margin-top:8px;"></div></div>
    <div id="dash" class="hidden">
      <div class="box">
        <h3 style="margin-bottom:10px;">🤖 Master Auto-Pilot &amp; C-Suite Controls</h3>
        <button class="purple" onclick="runCmd('/autopilot/run','Running Full Daily Auto-Pilot...')">🤖 Full Auto-Pilot</button>
        <button class="purple" onclick="runCmd('/csuite/run','Running C-Suite Board...')">🏛️ C-Suite Board</button>
        <button class="cyan" onclick="runCmd('/scan/4x','Running 4x Industry Scan...')">🔄 4x Scan</button>
        <button onclick="runCmd('/hunter/scan','Scanning opportunities...')">🌍 Opportunity Scan</button>
        <button class="green" onclick="runCmd('/hunter/daily-venture','Creating Daily Venture...')">💡 Daily Venture</button>
        <button class="cyan" onclick="runCmd('/trade/match','Matching Buyers & Sellers...')">🤝 Trade Match</button>
        <button onclick="runCmd('/outreach/run','Running Email/WA Closer...')">📧 Email/WA Closer</button>
        <button class="green" onclick="runCmd('/media/create','Generating Motion Reel...')">🎬 Create Reel</button>
        <div id="cmdRes" class="item hidden"></div>
      </div>
      <div class="box"><h3 style="margin-bottom:10px;">💰 Treasury &amp; Wallets</h3><div id="wGrid" class="grid"></div></div>
      <div class="box"><h3>💳 Invoices (Accept / Reject)</h3><div id="invList"></div></div>
      <div class="box"><h3>🧬 Clone Agents</h3><div id="agList"></div></div>
      <div class="box"><h3>📋 CRM Leads</h3><div id="leadList"></div></div>
      <div class="box"><h3>🌍 Opportunities</h3><div id="oppList"></div></div>
      <div class="box"><h3>🛡️ Sentinel Logs</h3><div id="logList"></div></div>
    </div>
  </div>
  <script>
    let key=sessionStorage.getItem('av8_key')||'';if(key){document.getElementById('adminKey').value=key;loadDash();}
    async function loadDash(){const k=document.getElementById('adminKey').value.trim(),err=document.getElementById('authErr');err.textContent='';try{const r=await fetch('/dashboard',{headers:{'x-admin-key':k}});if(!r.ok){err.textContent='❌ Galat Admin Key!';return;}key=k;sessionStorage.setItem('av8_key',k);const d=await r.json();document.getElementById('authBox').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');const wg=document.getElementById('wGrid');wg.innerHTML='';(d.wallets||[]).forEach(w=>{const c=document.createElement('div');c.className='w-card';c.innerHTML=`<div style="font-size:12px;color:#94a3b8;">${w.display_name} (${w.allocation_percent}%)</div><div class="amt">₹${w.balance_inr}</div>`;wg.appendChild(c);});renderInv(d.recent_invoices||[]);renderList('agList',d.clone_agents,a=>`${a.agent_name} [${a.department}] — Tasks: ${a.tasks_completed}`,'No clones.');renderList('leadList',d.recent_leads,l=>`[${l.lead_type||''}|${l.temperature}] ${l.lead_name} (${l.contact}) — ${l.requirement}`,'No leads.');renderList('oppList',d.recent_opportunities,o=>`[${o.score}/100] ${o.title}`,'No opportunities.');renderList('logList',d.sentinel_logs,s=>`[${s.healed?'HEALED':'ALERT'}] ${s.module}: ${(s.error_text||'').slice(0,100)}`,'No errors.');}catch(e){err.textContent='Error';}}
    function renderInv(arr){const el=document.getElementById('invList');el.innerHTML='';arr.forEach(inv=>{const d=document.createElement('div');d.className='item';const s=document.createElement('span');s.textContent=`[${inv.status}] ${inv.invoice_id} | ${inv.client_name} | ₹${inv.amount_inr} | UTR:${inv.utr_number||'-'} `;d.appendChild(s);const a=document.createElement('a');a.href='/pay/'+inv.invoice_id;a.target='_blank';a.textContent='[Open] ';d.appendChild(a);if(inv.status!=='PAID'){const b=document.createElement('button');b.className='green';b.textContent='✅ Accept';b.onclick=async()=>{await fetch('/invoices/'+inv.invoice_id+'/approve',{method:'POST',headers:{'x-admin-key':key}});loadDash();};d.appendChild(b);const rb=document.createElement('button');rb.className='red';rb.textContent='❌ Reject';rb.onclick=async()=>{const rsn=prompt('Reason:');if(!rsn)return;await fetch('/invoices/'+inv.invoice_id+'/reject',{method:'POST',headers:{'Content-Type':'application/json','x-admin-key':key},body:JSON.stringify({reason:rsn})});loadDash();};d.appendChild(rb);}el.appendChild(d);});}
    function renderList(id,arr,fmt,empty){const el=document.getElementById(id);el.innerHTML='';if(!arr||!arr.length){const d=document.createElement('div');d.className='item';d.textContent=empty;el.appendChild(d);return;}arr.forEach(x=>{const d=document.createElement('div');d.className='item';d.textContent=fmt(x);el.appendChild(d);});}
    async function runCmd(ep,w){const b=document.getElementById('cmdRes');b.classList.remove('hidden');b.textContent=w;const r=await fetch(ep,{method:'POST',headers:{'x-admin-key':key}});b.textContent=JSON.stringify(await r.json(),null,2);loadDash();}
  </script>
</body>
</html>"""
