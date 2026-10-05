import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i in range(2980, 2990):
    print(f"{i+1}: {content[i]}")
print("==================")
for i in range(3095, 3105):
    print(f"{i+1}: {content[i]}")
