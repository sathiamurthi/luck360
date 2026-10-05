import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "const s3Targets =" in line:
        for j in range(i, i + 10):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
