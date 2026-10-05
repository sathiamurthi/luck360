import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read()

# Fix these specific missing $() wrappers
fixes = [
    (r'\btk-status\b', r"$('tk-status')"),
    (r'\btk-date\b', r"$('tk-date')"),
    (r'\btk-slot\b', r"$('tk-slot')"),
    (r'\btk-res\b', r"$('tk-res')"),
    (r'\btk-text\b', r"$('tk-text')"),
    (r'\btk-rep\b', r"$('tk-rep')"),
    (r'\btk-rate-super\b', r"$('tk-rate-super')"),
    (r'\btk-rate-box\b', r"$('tk-rate-box')")
]

# But we only want to fix them if they are not already inside a string or $()
# Actually, since javascript variable names can't contain dashes anyway, ANY occurrence of tk-something outside quotes is probably the error!
for f_old, f_new in fixes:
    # Look for tk-something not preceded by ' or " or (
    content = re.sub(r"(?<!['\"\(])" + f_old, f_new, content)

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed tk- variables!")
