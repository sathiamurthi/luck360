import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
start = 3073 - 1
end = 3150
print("STARTING FROM LINE 3073:")
for i in range(start, end):
    print(f"{i+1}: {content[i]}")
