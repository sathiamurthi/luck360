import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2930, 2945):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
