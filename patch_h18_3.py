import io

content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

for i, line in enumerate(content):
    if "return { d1, d2, d3, p1_val" in line and "h17_val };" in line:
        content[i] = line.replace("h17_val };", "h17_val, h18_val };")
        content.insert(i, "const h18_val = `${(d1 + d3 + 1) % 10}${(d1 + d2) % 10}${(d2 + d3) % 10}`;")
        break

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content))
print("Patched H18 algorithm successfully!")
