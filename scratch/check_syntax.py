import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No script tags found!")
    exit(1)

js = scripts[-1]

def clean_js(src):
    out = []
    i = 0
    n = len(src)
    in_single = False
    in_double = False
    in_backtick = False
    in_comment_single = False
    in_comment_multi = False
    brace_depth = 0
    backtick_stack = []
    
    while i < n:
        c = src[i]
        c2 = src[i:i+2]
        
        if in_comment_single:
            if c == '\n':
                in_comment_single = False
            i += 1
            continue
        if in_comment_multi:
            if c2 == '*/':
                in_comment_multi = False
                i += 2
                continue
            i += 1
            continue
        if in_single:
            if c == '\\':
                i += 2
                continue
            if c == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            if c == '\\':
                i += 2
                continue
            if c == '"':
                in_double = False
            i += 1
            continue
        if in_backtick:
            if c == '\\':
                i += 2
                continue
            if c2 == '${':
                out.append('(')
                backtick_stack.append('template_expr')
                i += 2
                continue
            if c == '`':
                in_backtick = False
            i += 1
            continue
            
        if c2 == '//':
            in_comment_single = True
            i += 2
            continue
        if c2 == '/*':
            in_comment_multi = True
            i += 2
            continue
        if c == "'":
            in_single = True
            i += 1
            continue
        if c == '"':
            in_double = True
            i += 1
            continue
        if c == '`':
            in_backtick = True
            i += 1
            continue
            
        if backtick_stack and c == '}':
            backtick_stack.pop()
            out.append(')')
            in_backtick = True
            i += 1
            continue

        out.append(c)
        i += 1
    return ''.join(out)

cleaned = clean_js(js)

stack = []
pairs = {')': '(', ']': '[', '}': '{'}
error = False
for idx, ch in enumerate(cleaned):
    if ch in '([{':
        stack.append((ch, idx))
    elif ch in ')]}':
        if not stack:
            print(f"Unmatched {ch} at char {idx}")
            error = True
            break
        top, top_idx = stack.pop()
        if pairs[ch] != top:
            print(f"Mismatched {top} at {top_idx} with {ch} at {idx}")
            snippet = cleaned[max(0, idx-80):min(len(cleaned), idx+80)]
            print("Context around error:\n", snippet)
            error = True
            break

if stack and not error:
    print(f"Unclosed brackets remaining: {len(stack)}")
    for s in stack[:5]:
        print("Unclosed:", s)
elif not error:
    print("ALL JAVASCRIPT BRACKETS AND BRACES ARE 100% BALANCED!")
