import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "ticket slip parser" in line:
        print(f"ticket slip parser at {i+1}")
