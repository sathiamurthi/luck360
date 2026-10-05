import io

def check_brackets(text):
    stack = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for char in line:
            if char in "{[(":
                stack.append((char, i+1))
            elif char in "}])":
                if not stack:
                    print(f"Unmatched {char} at line {i+1}")
                    return
                last, line_num = stack.pop()
                expected = {'{': '}', '[': ']', '(': ')'}[last]
                if char != expected:
                    print(f"Mismatched {char} at line {i+1} (expected {expected} to close {last} from line {line_num})")
                    return
    if stack:
        print("Unclosed brackets:")
        for char, line_num in stack:
            print(f"  {char} from line {line_num}")
    else:
        print("All brackets match perfectly!")

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
# We should probably strip out strings and template literals before checking!
# A simple regex to remove template literals:
import re
stripped = re.sub(r'`[^`]*`', '``', content)
stripped = re.sub(r'"[^"]*"', '""', stripped)
stripped = re.sub(r"'[^']*'", "''", stripped)
# Also remove comments!
stripped = re.sub(r'//.*', '', stripped)
stripped = re.sub(r'/\*.*?\*/', '', stripped, flags=re.DOTALL)

check_brackets(stripped)
