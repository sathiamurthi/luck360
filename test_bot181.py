import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(120, 150):
    if "h14" in content[i] or "h7" in content[i] or "h15" in content[i]:
        print(f"{i+1}: {content[i].strip()}")
