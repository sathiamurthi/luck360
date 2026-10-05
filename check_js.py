import io

def check_brackets(text):
    stack = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for char in line:
            if char in "{[(":
                stack.append((char, i))
            elif char in "}])":
                if not stack:
                    return f"Unmatched {char} at line {i+1}"
                top, top_line = stack.pop()
                if (top == '{' and char != '}') or (top == '[' and char != ']') or (top == '(' and char != ')'):
                    return f"Mismatched {char} at line {i+1}, expected match for {top} from line {top_line+1}"
    if stack:
        return f"Unclosed {stack[-1][0]} from line {stack[-1][1]+1}"
    return "Balanced!"

content = io.open('script1.js', 'r', encoding='utf-8').read()
# Wait, template strings ` ` can contain unescaped brackets! 
# So simple bracket checking won't work on JS.
print("Cannot reliably check JS brackets with simple stack due to strings/regex.")
