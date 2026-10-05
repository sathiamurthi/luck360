import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "timelineContainer.innerHTML" in line:
        start = i
        break
for j in range(start, start + 25):
    print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
