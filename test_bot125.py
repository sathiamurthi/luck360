import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "function extract3Digits" in line:
        for j in range(i, i+15):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
