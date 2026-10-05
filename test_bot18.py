import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "updateKeralaDates" in line:
        print(f"updateKeralaDates at {i+1}")
