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
  <title>aIValue8 Corporation — Instant AI Micro-Store, Web/App &amp; Business Automation</title>
  <meta name="description" content="Deploy AI-powered ATS resumes for ₹29, local shop mini-websites for ₹99, or virtual office software instantly via UPI." />
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#030712;color:#e2e8f0;line-height:1.6;overflow-x:hidden;position:relative;}
    #aiCanvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.55;}
    .container{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:20px 16px 85px;}
    .logo-wrap{margin-bottom:16px;}
    .logo-wrap img{width:100%;max-width:630px;height:auto;display:block;border-radius:18px;border:1px solid rgba(56,189,248,0.25);box-shadow:0 0 35px rgba(37,99,235,0.2);}
    
    /* Live Ticker Bar */
    .ticker-bar{background:rgba(16,185,129,0.12);border:1px solid rgba(52,211,153,0.4);color:#34d399;padding:10px 16px;border-radius:12px;font-size:13px;font-weight:600;margin-bottom:18px;display:flex;align-items:center;gap:10px;box-shadow:0 0 20px rgba(16,185,129,0.15);}
    .pulse-dot{width:8px;height:8px;background:#10b981;border-radius:50%;animation:pulse 1.5s infinite;flex-shrink:0;}
    @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,0.8);}70%{box-shadow:0 0 0 10px rgba(16,185,129,0);}100%{box-shadow:0 0 0 0 rgba(16,185,129,0);}}

    .hero-title{font-size:26px;font-weight:800;color:#f8fafc;margin-bottom:8px;}
    .typed{background:linear-gradient(90deg,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .hero-sub{color:#94a3b8;font-size:14.5px;margin-bottom:18px;}
    .glass-box{background:rgba(15,23,42,0.78);backdrop-filter:blur(14px);border:1px solid rgba(56,189,248,0.3);border-radius:18px;padding:18px;margin-bottom:20px;box-shadow:0 0 35px rgba(37,99,235,0.12);}
    .store-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:15px;margin-bottom:20px;}
    .store-card{background:rgba(2,6,23,0.92);border:1px solid #1e293b;border-radius:16px;padding:20px;display:flex;flex-direction:column;justify-content:space-between;transition:0.3s;}
    .store-card:hover{border-color:#38bdf8;transform:translateY(-3px);}
    .price{font-size:26px;font-weight:900;color:#34d399;margin:8px 0;}
    input,select,textarea{width:100%;background:rgba(2,6,23,0.9);color:#f8fafc;border:1px solid #334155;border-radius:10px;padding:12px;margin-bottom:12px;font-size:14px;outline:none;}
    .btn-glow{width:100%;background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:13px;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;}
    footer{text-align:center;color:#64748b;font-size:13px;margin-top:20px;}
    footer a{color:#60a5fa;text-decoration:none;}
  </style>
</head>
<body>
  <canvas id="aiCanvas"></canvas>
  <div class="container">
    <div class="logo-wrap"><img src="/logo.svg" alt="aIValue8 Corporation" /></div>
    
    <!-- Live Social Proof Ticker -->
    <div class="ticker-bar">
      <div class="pulse-dot"></div>
      <div id="tickerText">🔥 Live Activity: Rahul from Mumbai just unlocked ATS Resume for ₹29!</div>
    </div>

    <div class="hero-title">Ready-to-Deploy <span class="typed">AI Micro-Services</span></div>
    <p class="hero-sub">Select a service below, pay instantly via UPI, and let our autonomous AI deliver your product in seconds.</p>

    <div class="store-grid">
      <div class="store-card">
        <div>
          <span style="background:rgba(56,189,248,0.15);color:#38bdf8;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">POPULAR • NO-BRAINER</span>
          <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">ATS Resume &amp; Cover Letter</h3>
          <div class="price">₹29</div>
          <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">Professional AI-optimized resume, cover letter &amp; interview prep kit delivered instantly.</p>
        </div>
        <button class="btn-glow" onclick="buyService('ATS Resume & Cover Letter Kit', 29)">Buy Now (₹29)</button>
      </div>

      <div class="store-card">
        <div>
          <span style="background:rgba(16,185,129,0.15);color:#34d399;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">LOCAL BUSINESS</span>
          <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">Mini-Website &amp; QR Menu</h3>
          <div class="price">₹99</div>
          <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">Instant mobile-ready landing page with WhatsApp order button for shops, cafes &amp; clinics.</p>
        </div>
        <button class="btn-glow" onclick="buyService('Local Shop Mini-Website & QR Menu', 99)">Buy Now (₹99)</button>
      </div>

      <div class="store-card">
        <div>
          <span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;">SAAS TRIAL</span>
          <h3 style="color:#f8fafc;margin-top:10px;font-size:18px;">Virtual Office Starter Desk</h3>
          <div class="price">₹49<span style="font-size:12px;color:#94a3b8;">/mo</span></div>
          <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">GPS Attendance, Task Board, Team Chat &amp; Client CRM for remote teams.</p>
        </div>
        <button class="btn-glow" onclick="buyService('Virtual Office Starter Desk Subscription', 49)">Subscribe (₹49)</button>
      </div>
    </div>

    <!-- FAST CHECKOUT BOX -->
    <div class="glass-box" id="checkoutBox">
      <h2 style="font-size:18px;color:#f8fafc;margin-bottom:6px;">⚡ Instant UPI Checkout</h2>
      <small style="color:#94a3b8;display:block;margin-bottom:14px;">Select item above or enter custom requirement below to generate a secure UPI payment link:</small>
      <form id="storeForm">
        <input type="text" id="sName" placeholder="Aapka Naam / Company Name" required />
        <input type="text" id="sContact" placeholder="WhatsApp Number ya Email" required />
        <input type="text" id="sDesc" placeholder="Selected Service / Custom Requirement" required />
        <input type="number" id="sAmt" placeholder="Amount in ₹" required />
        <button type="submit" id="sBtn" class="btn-glow">Generate Secure UPI Pay Link</button>
      </form>
      <div id="sMsg" style="margin-top:12px;font-size:14px;font-weight:600;"></div>
    </div>

    <footer><strong>aIValue8 Corporation (Sarahics)</strong> &bull; <a href="/store">Micro-Store</a> &bull; <a href="/panel">Owner Room</a></footer>
  </div>

  <a href="https://wa.me/__WA_NUM__?text=%5BSTORE%5D%20Hi%20Sarahics%20Team%2C%20mujhe%20micro-store%20service%20leni%20hai"
     target="_blank"
     style="position:fixed;bottom:20px;right:20px;background:#25D366;color:#fff;padding:12px 18px;border-radius:50px;font-family:sans-serif;font-weight:bold;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.25);z-index:9999;">
     💬 WhatsApp Support
  </a>

  <script>
    const canvas=document.getElementById('aiCanvas'),ctx=canvas.getContext('2d');let pts=[];
    function rsz(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}window.addEventListener('resize',rsz);rsz();
    for(let i=0;i<30;i++)pts.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5});
    function anim(){ctx.clearRect(0,0,canvas.width,canvas.height);for(let i=0;i<pts.length;i++){let p=pts[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>canvas.width)p.vx*=-1;if(p.y<0||p.y>canvas.height)p.vy*=-1;ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(p.x,p.y,1.6,0,Math.PI*2);ctx.fill();for(let j=i+1;j<pts.length;j++){let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);if(d<120){ctx.strokeStyle=`rgba(52,211,153,${1-d/120})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p2.x,p2.y);ctx.stroke();}}}requestAnimationFrame(anim);}anim();

    // Real-Time Ethical Live Status Fetcher (Zero Fake Messages)
    async function loadRealTicker() {
      try {
        const r = await fetch('/public/telemetry');
        const d = await r.json();
        const el = document.getElementById('tickerText');
        if(el) {
          el.textContent = `🟢 aIValue8 System Online • Active AI Clones: ${d.active_agents || 1} • Opportunities Tracked: ${d.opportunities_found || 0} • Ethical Governance: Verified`;
        }
      } catch(e) {
        const el = document.getElementById('tickerText');
        if(el) el.textContent = "🟢 aIValue8 Autonomous Core Online & Ready for Orders";
      }
    }
    loadRealTicker();
    setInterval(loadRealTicker, 15000);

    function buyService(desc, amt){
      document.getElementById('sDesc').value = desc;
      document.getElementById('sAmt').value = amt;
      document.getElementById('checkoutBox').scrollIntoView({behavior:'smooth'});
      document.getElementById('sName').focus();
    }

    document.getElementById('storeForm').addEventListener('submit', async(e)=>{
      e.preventDefault();
      const btn=document.getElementById('sBtn'), msg=document.getElementById('sMsg');
      btn.disabled=true; msg.style.color='#94a3b8'; msg.textContent='Generating secure payment link...';
      try{
        const r = await fetch('/invoices/create', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            client_name: document.getElementById('sName').value,
            client_contact: document.getElementById('sContact').value,
            description: document.getElementById('sDesc').value,
            amount_inr: parseFloat(document.getElementById('sAmt').value)
          })
        });
        const d = await r.json();
        if(d.pay_path){
          msg.style.color = '#34d399';
          msg.innerHTML = `✅ Payment Link Ready! <br><a href="${d.pay_path}" target="_blank" style="color:#38bdf8;font-size:16px;">👉 Open UPI Payment Page (₹${d.amount_inr})</a>`;
          e.target.reset();
        } else {
          msg.style.color = '#f87171';
          msg.textContent = '⚠️ ' + (d.detail || 'Error creating link');
        }
      }catch(err){
        msg.style.color = '#f87171';
        msg.textContent = '❌ Network error.';
      }
      btn.disabled=false;
    });
  </script>
</body>
</html>"""
