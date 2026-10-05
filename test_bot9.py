import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2895, 2905):
    print(f"{i+1}: {content[i]}")
print("==================")
for i in range(3010, 3020):
    print(f"{i+1}: {content[i]}")
