import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("Full Daily Audit (September 2026 - Kerala Chart Matches)")
print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
