import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "const d1 =" in line or "let d1 =" in line:
        print(f"{i+1}: {line.strip()}")
