import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i in range(580, 610):
    if "Dual Confluence" in content[i] or "Your discovered" in content[i] or "Head H8" in content[i] or "From previous" in content[i]:
        print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
