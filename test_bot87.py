import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "function pollLiveDatabase" in line:
        print(f"Found at {i+1}")
        break
