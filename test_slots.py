import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "const slots = [" in line or "let slots = [" in line:
        start = i
        print(f"Found at {i+1}")
        for j in range(start, start + 30):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
