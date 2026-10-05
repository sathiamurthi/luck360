import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
count = 0
for i, line in enumerate(content):
    if "NEW: Absolute Subtraction Card" in line:
        count += 1
        print(f"Found at {i+1}")
print(f"Total count: {count}")
