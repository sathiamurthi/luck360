import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "const slots = [" in line or "let slots = [" in line:
        start = i
        break
print(content[start-1].strip())
for j in range(start, start + 3):
    print(content[j].strip())
