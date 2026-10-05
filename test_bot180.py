import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "const h14 = " in line or "const h7 = " in line:
        print(f"{i+1}: {line.strip()}")
