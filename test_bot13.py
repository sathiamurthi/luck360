import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

for x in range(1, 200):
    l1 = content[2898 - 1 - x].strip()
    l2 = content[3011 - 1 - x].strip()
    if l1 != l2:
        print(f"Mismatch at offset {x}")
        print(f"First copy line {2898 - x}: {l1}")
        print(f"Second copy line {3011 - x}: {l2}")
        break
