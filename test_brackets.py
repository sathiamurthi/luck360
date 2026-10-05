import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

def check_brackets(text):
    stack = []
    line_num = 1
    in_string = False
    string_char = ''
    in_comment = False
    in_multiline_comment = False
    escape = False

    i = 0
    while i < len(text):
        char = text[i]
        
        if char == '\n':
            line_num += 1
            if in_comment:
                in_comment = False
        
        if escape:
            escape = False
            i += 1
            continue
            
        if char == '\\':
            escape = True
            i += 1
            continue

        if not in_string and not in_comment and not in_multiline_comment:
            if char == '/' and i + 1 < len(text):
                if text[i+1] == '/':
                    in_comment = True
                    i += 1
                elif text[i+1] == '*':
                    in_multiline_comment = True
                    i += 1
            elif char in ("'", '"', '`'):
                in_string = True
                string_char = char
            elif char == '{':
                stack.append(('{', line_num))
            elif char == '}':
                if not stack:
                    print(f"Extra closing }} at line {line_num}")
                else:
                    last = stack.pop()
                    if last[0] != '{':
                        print(f"Mismatched closing }} at line {line_num}, expected {last[0]}")
        elif in_string:
            if char == string_char:
                in_string = False
        elif in_multiline_comment:
            if char == '*' and i + 1 < len(text) and text[i+1] == '/':
                in_multiline_comment = False
                i += 1
                
        i += 1
    
    if stack:
        print(f"Unclosed braces left over: {len(stack)}. First unclosed at line {stack[0][1]}")
    else:
        print("Braces match perfectly!")

check_brackets(content)
