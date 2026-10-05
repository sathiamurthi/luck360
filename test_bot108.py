import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "timelineContainer.innerHTML" in line:
        print(f"timelineContainer at {i+1}")
