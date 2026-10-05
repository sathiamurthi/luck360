import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "let h1 =" in line or "const h1 =" in line or "h1 =" in line:
        print(f"{i+1}: {line.strip()}")
