import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "async function sync()" in line:
        print(f"sync() at {i+1}")
