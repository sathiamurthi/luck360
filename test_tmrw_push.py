import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "is8PMComplete" in line and "slots.push" in content[i+1]:
        start = i
        for j in range(start, start + 30):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
