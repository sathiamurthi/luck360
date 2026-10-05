import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i in range(110, 130):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
