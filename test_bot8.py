import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2910, 2930):
    print(f"{i+1}: {content[i]}")
