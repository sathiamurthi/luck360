import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
print(f"Total lines: {len(content)}")
