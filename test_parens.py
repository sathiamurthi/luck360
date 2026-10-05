import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

def check_parens(text):
    stack = []
    line_num = 1
    in_string = False
    string_char = ''
    in_comment = False
    in_multiline_comment = False
    in_regex = False
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

        if not in_string and not in_comment and not in_multiline_comment and not in_regex:
            if char == '/' and i + 1 < len(text) and text[i+1] == '/':
                in_comment = True
                i += 1
            elif char == '/' and i + 1 < len(text) and text[i+1] == '*':
                in_multiline_comment = True
                i += 1
            elif char in ("'", '"', '`'):
                in_string = True
                string_char = char
            # Very basic regex detection (flawed but catches some)
            elif char == '/':
                # check prev char to see if it's likely a regex (e.g. =, (, ,)
                prev_idx = i - 1
                while prev_idx >= 0 and text[prev_idx] in ' \t\n':
                    prev_idx -= 1
                if prev_idx >= 0 and text[prev_idx] in '=,([':
                    in_regex = True
            elif char == '(':
                stack.append(('(', line_num))
            elif char == ')':
                if not stack:
                    pass # ignore extra for now
                else:
                    stack.pop()
        elif in_string:
            if char == string_char:
                in_string = False
            elif char == '$' and string_char == '`' and i + 1 < len(text) and text[i+1] == '{':
                # Javascript template literal interpolation `${...}`
                # We can't handle nested braces easily here, let's just ignore
                pass
        elif in_regex:
            if char == '/':
                in_regex = False
        elif in_multiline_comment:
            if char == '*' and i + 1 < len(text) and text[i+1] == '/':
                in_multiline_comment = False
                i += 1
                
        i += 1
    
    if stack:
        print(f"Unclosed parens left over: {len(stack)}. First unclosed at line {stack[0][1]}")
    else:
        print("Parens match perfectly!")

check_parens(content)
