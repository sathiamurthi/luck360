import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "dynamic_prev_tail = t1" in line:
        start = max(0, i - 5)
        for j in range(start, start + 25):
            print(f"{j+1}: {content[j].encode('ascii', 'ignore').decode('ascii')}")
        break
