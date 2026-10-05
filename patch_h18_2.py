import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""const h17_3 = d3;
const h17_val = `\$\{h17_1\}\$\{h17_2\}\$\{h17_3\}`;

return \{ d1, d2, d3, p1_val, p2_conv1, p2_conv2, p3_val, r41_val, trans_val, h1_val, h2_val, h3_val, h4_val, h4_rev_ab, h6_val, h7_val, h8_val, h9_val, h10_val, h11_val, h12_val, h13_val, h14_val, h15_val, h16_val, h16_pal_val, h17_val \};"""

replacement = """const h17_3 = d3;
const h17_val = `${h17_1}${h17_2}${h17_3}`;

// USER NEW PATTERN H18: Cross-Sum Bridging Rule
const h18_val = `${(d1 + d3 + 1) % 10}${(d1 + d2) % 10}${(d2 + d3) % 10}`;

return { d1, d2, d3, p1_val, p2_conv1, p2_conv2, p3_val, r41_val, trans_val, h1_val, h2_val, h3_val, h4_val, h4_rev_ab, h6_val, h7_val, h8_val, h9_val, h10_val, h11_val, h12_val, h13_val, h14_val, h15_val, h16_val, h16_pal_val, h17_val, h18_val };"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched H18 algorithm successfully!")
else:
    print("Target block not found.")
