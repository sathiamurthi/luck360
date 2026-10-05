import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "const row=(j)=>" in line:
        for j in range(i-5, i+10):
            print(f"{j+1}: {content[j].strip().encode('ascii', 'ignore').decode('ascii')}")
        break
