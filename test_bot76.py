import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "is8PMComplete" in line and "function" in content[i-5:i+5]:
        pass
    if "is8PMComplete" in line:
        print(f"{i+1}: {line.strip()}")
