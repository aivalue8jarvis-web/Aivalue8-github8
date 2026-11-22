WORKSPACE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>aIValue8 Client Generative Workspace</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
    body{background:#030712;color:#e2e8f0;padding:20px;line-height:1.6;}
    .wrap{max-width:900px;margin:0 auto;}
    .header{background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:22px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}
    h1{font-size:24px;color:#38bdf8;}
    .card{background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:20px;margin-bottom:16px;}
    .card h3{color:#34d399;margin-bottom:10px;font-size:18px;}
    input,textarea{width:100%;background:#020617;color:#fff;border:1px solid #334155;border-radius:10px;padding:12px;margin-bottom:12px;font-size:14px;outline:none;}
    .btn{background:linear-gradient(90deg,#2563eb,#10b981);color:#fff;border:none;padding:12px 20px;border-radius:10px;font-weight:700;cursor:pointer;}
    .preview-frame{width:100%;height:450px;background:#020617;border:1px solid #334155;border-radius:12px;margin-top:10px;}
    a{color:#60a5fa;text-decoration:none;}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div>
        <h1>🏢 aIValue8 Client Generative Workspace</h1>
        <p style="color:#94a3b8;font-size:13px;">AI-Native Live Interactive Dashboard &amp; Project Hub</p>
      </div>
      <div><a href="/" class="btn" style="padding:10px 16px;font-size:13px;">← Home Portal</a></div>
    </div>

    <div class="card">
      <h3>💬 Live AI Project Assistant</h3>
      <p style="color:#94a3b8;font-size:13.5px;margin-bottom:12px;">Apne active project ya order ke baare mein yahan AI se direct baat karein ya update maangein:</p>
      <textarea id="clientPrompt" rows="2" placeholder="Jaise: 'Mere ATS resume ka status kya hai?' ya 'Mini-website mein phone number change karna hai'..."></textarea>
      <button class="btn" onclick="askWorkspaceAI()">Ask AI Assistant</button>
      <div id="aiResponse" class="card" style="display:none;margin-top:12px;background:#020617;"></div>
    </div>

    <div class="card">
      <h3>🚀 Live Deployed Assets &amp; Previews</h3>
      <p style="color:#94a3b8;font-size:13.5px;margin-bottom:10px;">Aapka generate kiya gaya digital asset yahan live render hota hai:</p>
      <input type="text" id="assetSlug" placeholder="Enter slug (e.g. p-av8-xxxx or sharma-solar) and press Load" />
      <button class="btn" style="background:#2563eb;" onclick="loadAssetPreview()">Load Live Asset</button>
      <iframe id="assetViewer" class="preview-frame" src="about:blank"></iframe>
    </div>
  </div>

  <script>
    async function askWorkspaceAI() {
      const q = document.getElementById('clientPrompt').value.trim();
      if(!q) return;
      const resBox = document.getElementById('aiResponse');
      resBox.style.display = 'block';
      resBox.textContent = 'AI thinking...';
      try {
        const r = await fetch('/ask', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({user_message: q, source: 'client-workspace'})
        });
        const d = await r.json();
        resBox.textContent = d.reply || 'No response';
      } catch(e) {
        resBox.textContent = 'Connection error.';
      }
    }

    function loadAssetPreview() {
      const slug = document.getElementById('assetSlug').value.trim();
      if(!slug) return;
      document.getElementById('assetViewer').src = '/p/' + slug;
    }
  </script>
</body>
</html>
"""
