import io
import re

text = io.open('script1.js', 'r', encoding='utf-8').read()
text = re.sub(r'//.*', '', text)
text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
text = re.sub(r'"(\\"|[^"])*"', '""', text)
text = re.sub(r"'(\\'|[^'])*'", "''", text)

# Let's remove template literals completely but carefully
while '`' in text:
    start = text.find('`')
    end = text.find('`', start + 1)
    # We must skip escaped backticks!
    while end != -1 and text[end-1] == '\\':
        end = text.find('`', end + 1)
    if end == -1:
        print("Unclosed template literal!")
        break
    # For simplicity, if there are ${ inside, we might remove the braces!
    # But those braces inside ${} are part of JS expressions.
    # If we remove the whole `...`, we lose checking those expressions!
    # But if the error is outside, it's fine.
    text = text[:start] + '``' + text[end+1:]

stack = []
for i, c in enumerate(text):
    if c in '{[(':
        stack.append((c, i))
    elif c in '}])':
        if not stack:
            print(f"Unmatched {c} at {i}")
            break
        top, pos = stack.pop()
        pairs = {'}':'{', ']':'[', ')':'('}
        if top != pairs[c]:
            print(f"Mismatched {c} at {i}. Expected closing for {top} at {pos}")
            break
if stack:
    print(f"Unclosed: {stack[-1]}")
else:
    print("No bracket errors found outside template literals!")
