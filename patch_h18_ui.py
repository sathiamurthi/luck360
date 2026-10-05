import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

# Replace all occurrences of h7_val}</span></span> with h7_val}</span></span> <span class="font-bold text-amber-800">H18: <span class="font-black text-amber-950">${bPats.h18_val || '---'}</span></span> etc.

def replacer(match):
    color = match.group(1) # amber, emerald, indigo, rose
    pats = match.group(2)  # bPats, bHeadPats, cPats, cHeadPats
    full = match.group(0)
    return f'{full}\n<span class="font-bold text-{color}-800">H18: <span class="font-black text-{color}-950">${{{pats}.h18_val || \'---\'}}</span></span>'

# This matches the H7 column specifically for all 4 types
pattern = r'<span class="font-bold text-([a-z]+)-800">H7: <span class="font-black text-\1-950">\$\{([a-zA-Z]+)\.h7_val \|\| \'---\'\}</span></span>'

new_content = re.sub(pattern, replacer, content)

# Also update the initialization objects:
new_content = new_content.replace("{ h17_val: '---', h15_val: '---', h14_val: '---', h7_val: '---' }", "{ h17_val: '---', h15_val: '---', h14_val: '---', h7_val: '---', h18_val: '---' }")

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(new_content)
print("Patched H18 into UI successfully!")
