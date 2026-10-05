import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2945, 3175):
    line = content[i].strip()
    if line.startswith('function') and 'tk' not in line.lower():
        print(f"{i+1}: {line}")
