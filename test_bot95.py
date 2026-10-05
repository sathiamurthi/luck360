import io
import traceback
try:
    with io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
        content = f.read()
    # Try parsing it via regex for mismatched braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    print(f"Braces: {open_braces} open, {close_braces} close")
    open_parens = content.count('(')
    close_parens = content.count(')')
    print(f"Parens: {open_parens} open, {close_parens} close")
except Exception as e:
    print(e)
