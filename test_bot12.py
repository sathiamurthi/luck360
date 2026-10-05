import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

# Let's see if line 3011 - x == line 2898 - x
for x in range(1, 200):
    if content[3011 - 1 - x] != content[2898 - 1 - x]:
        print(f"Mismatch at offset {x}")
        print(f"First copy line {2898 - x}: {content[2898 - 1 - x]}")
        print(f"Second copy line {3011 - x}: {content[3011 - 1 - x]}")
        break
