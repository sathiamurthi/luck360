import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content[2950:3005]):
    if "function load" in line or "function save" in line or "function ocr" in line:
        print(f"Found {line.strip()} at {2950+i+1}")
