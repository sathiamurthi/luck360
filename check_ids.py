import io
import re

html_content = io.open('index.html', 'r', encoding='utf-8').read()
js_content = io.open('script1.js', 'r', encoding='utf-8').read()

ids_in_html = set(re.findall(r'id="([^"]+)"', html_content))
ids_in_js = set(re.findall(r'getElementById\([\'"]([^\'"]+)[\'"]\)', js_content))

missing_ids = []
for js_id in ids_in_js:
    if js_id not in ids_in_html:
        missing_ids.append(js_id)

print("Missing IDs from HTML that JS tries to get:")
for mid in missing_ids:
    print(mid)
