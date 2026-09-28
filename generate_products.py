import os
import json
import urllib.request

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY missing!")
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Error: {e}")
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
        filename = f"products/product_{idx}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(raw_p.strip())
        products_data.append({"id": idx, "content": raw_p.strip()})

# Generate index.html dashboard
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatCommerce - Automated Products</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
        pre { background: #0f172a; padding: 10px; border-radius: 6px; white-space: pre-wrap; height: 180px; overflow-y: auto; color: #cbd5e1; }
        a { display: block; text-align: center; background: #38bdf8; color: #0f172a; font-weight: bold; padding: 10px; border-radius: 8px; text-decoration: none; margin-top: 10px; }
    </style>
</head>
<body>
    <h1 style="text-align: center; color: #38bdf8;">🚀 ChatCommerce Products Dashboard</h1>
    <div class="grid">
"""

for p in products_data:
    html_content += f"""
        <div class="card">
            <h3>Product #{p['id']}</h3>
            <pre>{p['content'][:300]}...</pre>
            <a href="products/product_{p['id']}.md">View Details & Script</a>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
