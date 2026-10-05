import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
print("Total lines:", len(content))
for i in range(3165, min(3175, len(content))):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
