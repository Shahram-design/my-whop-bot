import os
import json
import urllib.request

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY missing!")
        return None
    
    # Correct updated Gemini API Endpoint
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API Error: {e}")
        return None

os.makedirs("products", exist_ok=True)

prompt = """
Generate 5 high-converting digital products for Whop store / ChatCommerce.
For each product, provide:
1. Title
2. Target Price ($3.99 - $14.99)
3. Category / Niche
4. Description
5. TikTok / Instagram Reels Script (Visuals + Voiceover)
6. Captions & Hashtags

Separate each product with '---PRODUCT---'.
"""

gen_output = get_gemini_response(prompt)
products_data = []

if gen_output:
    raw_products = gen_output.split("---PRODUCT---")
    for idx, raw_p in enumerate(raw_products[:5], 1):
        if raw_p.strip():
            products_data.append({"id": idx, "content": raw_p.strip()})
else:
    # Backup Fallback
    for idx in range(1, 6):
        content = f"# Digital Product {idx}: Automation Toolkit\n\nPrice: ${4.99 + idx}\n\n## Description\nComplete guide for digital automation.\n\n## Script\nVisual: Dynamic preview of digital dashboard.\nVoiceover: Grow your ChatCommerce business on autopilot!\n\n#chatcommerce #automation"
        products_data.append({"id": idx, "content": content})

# 1. Generate Product HTML Details Pages with Direct Back Link
for p in products_data:
    filename = f"products/product_{p['id']}.html"
    p_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product #{p['id']} Details</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; max-width: 800px; margin: 0 auto; }}
        .btn {{ display: inline-block; background: #38bdf8; color: #0f172a; font-weight: bold; padding: 10px 18px; border-radius: 8px; text-decoration: none; margin-bottom: 20px; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 24px; border: 1px solid #334155; line-height: 1.6; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <a href="https://shahram-design.github.io/my-whop-bot/" class="btn">← Back to Dashboard</a>
    <div class="card">{p['content']}</div>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(p_html)

# 2. Generate Main Dashboard (index.html)
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatCommerce - Automated Products</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; margin: 0; }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 30px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; display: flex; flex-direction: column; justify-content: space-between; }
        pre { background: #0f172a; padding: 12px; border-radius: 8px; white-space: pre-wrap; height: 160px; overflow-y: auto; color: #cbd5e1; font-size: 14px; }
        .btn { display: block; text-align: center; background: #38bdf8; color: #0f172a; font-weight: bold; padding: 12px; border-radius: 8px; text-decoration: none; margin-top: 15px; }
    </style>
</head>
<body>
    <h1>🚀 ChatCommerce Products Dashboard</h1>
    <div class="grid">
"""

for p in products_data:
    html_content += f"""
        <div class="card">
            <h3>Product #{p['id']}</h3>
            <pre>{p['content'][:250]}...</pre>
            <a href="products/product_{p['id']}.html" class="btn">View Details & Script</a>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
