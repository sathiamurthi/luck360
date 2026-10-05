import io
content = io.open('index.html', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "What Produced Every Result" in line:
        print(f"Found in index.html at line {i+1}")
