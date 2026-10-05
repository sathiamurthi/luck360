import io

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
new_content = []

in_duplicate_block = False
duplicate_braces = 0
found_first = False

for line in content:
    if "// INJECT 4 SUBCARDS" in line:
        if not found_first:
            found_first = True
            new_content.append(line)
        else:
            in_duplicate_block = True
            duplicate_braces = 0
            # Wait, the block starts with `// INJECT`. The `{` happens on the `if` line below it.
            # So I should just ignore lines until the `{` matches!
            # Let's just use a simple state machine.
            pass
    elif in_duplicate_block:
        if "{" in line:
            duplicate_braces += line.count("{")
        if "}" in line:
            duplicate_braces -= line.count("}")
        
        if duplicate_braces <= 0 and "}" in line: # It closed!
            in_duplicate_block = False
    else:
        new_content.append(line)

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write('\n'.join(new_content))
print("Removed duplicate subcards injections!")
