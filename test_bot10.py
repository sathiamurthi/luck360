import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "MULTI-PATTERN DETECTOR ALGORITHM" in line:
        print(f"MULTI-PATTERN at {i+1}")
