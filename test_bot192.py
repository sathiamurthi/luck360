import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "Check against actual results" in line or "Reverse Prev" in line:
        for j in range(i-5, i+15):
            print(f"{j+1}: {content[j].strip()}")
        break
