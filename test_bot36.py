import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(len(content)-20, len(content)):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
