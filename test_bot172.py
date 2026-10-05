import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
# Replace ALL template literals `...` with ` `
content = re.sub(r'`[^`]*`', '``', content, flags=re.DOTALL)
# Replace ALL strings "..." with ""
content = re.sub(r'"([^"\\]|\\.)*"', '""', content)
# Replace ALL strings '...' with ''
content = re.sub(r"'([^'\\]|\\.)*'", "''", content)
# Remove comments
content = re.sub(r'//.*', '', content)
content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

stack = []
lines = content.splitlines()
for i, line in enumerate(lines):
    for char in line:
        if char in "{[(":
            stack.append((char, i+1))
        elif char in "}])":
            if not stack:
                print(f"Unmatched {char} at line {i+1}")
                exit(1)
            last, line_num = stack.pop()
            expected = {'{': '}', '[': ']', '(': ')'}[last]
            if char != expected:
                print(f"Mismatched {char} at line {i+1} (expected {expected} to close {last} from line {line_num})")
                exit(1)

if stack:
    print("Unclosed brackets:")
    for char, line_num in stack[-5:]:
        print(f"  {char} from line {line_num}")
else:
    print("Syntax matches perfectly!")
