import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "Dual Confluence" in line:
        print(f"Found in script1.js at line {i+1}")
