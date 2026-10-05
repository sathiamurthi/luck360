import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""const h17_3 = d3;
const h17_val = `\$\{h17_1\}\$\{h17_2\}\$\{h17_3\}`;"""

replacement = """const h17_3 = d3;
const h17_val = `${h17_1}${h17_2}${h17_3}`;

// USER NEW PATTERN H18: Cross-Sum Bridging Rule (Hits 728 -> 690)
const h18_val = `${(d1 + d3 + 1) % 10}${(d1 + d2) % 10}${(d2 + d3) % 10}`;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched H18 algorithm successfully!")
else:
    print("Target block not found.")
