import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2995, 3015):
    print(f"{i+1}: {content[i]}")
