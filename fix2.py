import io
def fix_mojibake(text):
    fixed_bytes = bytearray()
    for char in text:
        try:
            b = char.encode('cp1252')
            fixed_bytes.extend(b)
        except UnicodeEncodeError:
            fixed_bytes.extend(char.encode('utf-8'))
    
    return fixed_bytes.decode('utf-8', errors='replace')

text = io.open('index.html', 'r', encoding='utf-8').read()
new_text = fix_mojibake(text)
io.open('index.html', 'w', encoding='utf-8').write(new_text)
