import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "NEW: Absolute Subtraction Card" in line:
        start = max(0, i - 15)
        for j in range(start, i + 25):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
