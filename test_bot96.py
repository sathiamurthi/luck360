import io
with io.open('all_scripts.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    content = f.read()
open_braces = content.count('{')
close_braces = content.count('}')
print(f"Backup Braces: {open_braces} open, {close_braces} close")
open_parens = content.count('(')
close_parens = content.count(')')
print(f"Backup Parens: {open_parens} open, {close_parens} close")
