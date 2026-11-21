LEGAL_CSS = "body{background:#030712;color:#e2e8f0;font-family:sans-serif;padding:24px;line-height:1.7;}.w{max-width:760px;margin:0 auto;background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:26px;}h1{color:#38bdf8;margin-bottom:14px;}h3{color:#34d399;margin:16px 0 6px;}p{color:#cbd5e1;font-size:14.5px;margin-bottom:10px;}a{color:#60a5fa;}"

def wrap_legal(title: str, body: str) -> str:
    return f"<!DOCTYPE html><html><head><meta charset='UTF-8'/><meta name='viewport' content='width=device-width,initial-scale=1.0'/><title>{title} — aIValue8 (Sarahics)</title><link rel='icon' type='image/svg+xml' href='/icon.svg'/><style>{LEGAL_CSS}</style></head><body><div class='w'><h1>{title}</h1>{body}<br><p><a href='/'>← Back to Home</a> | <a href='/store'>Micro-Store</a></p></div></body></html>"

PRIVACY_HTML = wrap_legal("Privacy Policy", """
<p><strong>aIValue8 Corporation (Sarahics)</strong> respects your privacy and complies with India's Digital Personal Data Protection (DPDP) Act, 2023.</p>
<h3>1. Data We Collect</h3>
<p>We collect only the name, email/WhatsApp contact, and service requirements voluntarily submitted by users for delivering digital services, ATS resumes, mini-websites, or business inquiries.</p>
<h3>2. Payment Security</h3>
<p>We never store raw debit/credit card numbers or UPI PINs. Payments are processed via direct UPI or RBI-authorized payment gateways.</p>
<h3>3. Contact &amp; Data Removal</h3>
<p>To update or delete your data, email us at <strong>sales@sarahics.in</strong> or <strong>ceo@sarahics.in</strong>.</p>
""")

TERMS_HTML = wrap_legal("Terms & Conditions", """
<p>By accessing <strong>https://sarahics.in</strong> and ordering services from <strong>aIValue8 Corporation (Sarahics)</strong>, you agree to the following terms:</p>
<h3>1. Nature of Services</h3>
<p>We provide digital AI automation tools, ATS resume preparation, mini-website generation, and Digital Virtual Office workplace software (task &amp; attendance management).</p>
<h3>2. Virtual Office Software Disclaimer</h3>
<p>Our Digital Virtual Office SaaS is an online workplace management software. It does NOT provide physical office addresses for GST or MCA company registration.</p>
<h3>3. Ethical Use &amp; Governing Law</h3>
<p>All services are governed by the laws of India. Any illegal, fraudulent, or spam requests are strictly prohibited.</p>
""")

REFUND_HTML = wrap_legal("Refund & Cancellation Policy", """
<h3>1. Digital Services &amp; Micro-Store Orders</h3>
<p>Since ATS resumes, mini-websites, and AI reports are custom digital products generated immediately after payment verification, orders once delivered are generally non-refundable.</p>
<h3>2. Failed / Undelivered Orders</h3>
<p>If payment is debited and your digital service is not delivered within 24 hours, or if there is a verified technical failure on our end, a <strong>100% refund</strong> will be processed to your original UPI/bank account within <strong>5–7 working days</strong>.</p>
<h3>3. Subscriptions</h3>
<p>Monthly Digital Virtual Office software trials (₹49/mo) can be cancelled anytime before the next billing cycle by emailing <strong>sales@sarahics.in</strong>.</p>
""")

CONTACT_HTML = wrap_legal("Contact Us & About Sarahics", """
<p><strong>Business Name:</strong> aIValue8 Corporation (Sarahics — Udyam Registered Digital Services)</p>
<p><strong>Website:</strong> https://sarahics.in</p>
<p><strong>Sales &amp; Order Support:</strong> sales@sarahics.in</p>
<p><strong>Executive &amp; Compliance:</strong> ceo@sarahics.in</p>
<p><strong>Support Hours:</strong> Monday to Saturday, 10:00 AM – 7:00 PM IST</p>
""")
