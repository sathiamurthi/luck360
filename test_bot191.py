import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "let multiplierHtml" in line:
        for j in range(i-20, i+20):
            print(f"{j+1}: {content[j].strip()}")
        break
