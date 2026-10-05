import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "const h15 =" in line or "const h15=" in line:
        for j in range(i-5, i+20):
            print(f"{j+1}: {content[j].strip()}")
        break
