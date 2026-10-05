import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i in range(1692, len(content)):
    if "is8PMComplete" in content[i]:
        print(f"{i+1}: {content[i].strip()}")
