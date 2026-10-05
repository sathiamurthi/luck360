import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "h15_val:" in line:
        for j in range(i-20, i+10):
            print(f"{j+1}: {content[j].strip()}")
        break
