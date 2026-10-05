import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content[-50:]):
    print(f"{len(content)-50+i+1}: {line}")
