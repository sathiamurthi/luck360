import sys
content = open('debug.js', 'r', encoding='utf-8').read()

def parse(text):
    stack = []
    in_str = False
    str_char = None
    escape = False
    
    # We will just strip out ALL strings and comments first to make bracket checking trivial!
    import re
    # strip line comments
    text = re.sub(r'//.*', '', text)
    # strip block comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # strip strings
    text = re.sub(r'"(\\"|[^"])*"', '""', text)
    text = re.sub(r"'(\\'|[^'])*'", "''", text)
    # strip backticks (might contain ${} but we ignore it if we strip it all!)
    # wait, ${} contains JS code which MIGHT contain brackets!
    # so we shouldn't strip backticks blindly. We should process character by character.
    
    i = 0
    in_tmpl = False
    tmpl_stack = []
    
    while i < len(text):
        c = text[i]
        
        if escape:
            escape = False; i += 1; continue
        if c == '\\':
            escape = True; i += 1; continue
            
        if in_str:
            if c == str_char:
                in_str = False
            i += 1
            continue
            
        if in_tmpl:
            if c == '`':
                in_tmpl = False
            elif c == '$' and i+1 < len(text) and text[i+1] == '{':
                tmpl_stack.append('{')
                stack.append(('{', i+1))
                i += 1
            i += 1
            continue
            
        if c in ["'", '"']:
            in_str = True
            str_char = c
            i += 1; continue
            
        if c == '`':
            in_tmpl = True
            i += 1; continue
            
        if c in '{[(':
            stack.append((c, i))
        elif c in '}])':
            if not stack: return f"Unmatched {c} at {i}"
            top, pos = stack.pop()
            pairs = {'}':'{', ']':'[', ')':'('}
            if top != pairs[c]: return f"Mismatched {c} at {i}. Expected closing for {top} at {pos}"
            if c == '}' and tmpl_stack and tmpl_stack[-1] == '{':
                tmpl_stack.pop()
                in_tmpl = True # back to template
        i += 1
            
    if stack: return f"Unclosed brackets left: {stack}"
    return "OK"

print(parse(content))
