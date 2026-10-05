import io

try:
    content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
    
    # We have some surrogates in the string.
    # Python 3 encodes surrogates into CESU-8 like byte sequences which are invalid UTF-8.
    # To fix this, we can encode with 'utf-16', and decode back, or just replace them!
    
    # Actually, we can encode to utf-16, then decode ignoring errors, then encode to utf-8.
    # But wait, Python strings are unicode. We can just encode to utf-8 with 'replace'.
    clean_bytes = content.encode('utf-8', errors='replace')
    
    with open('script1.js', 'wb') as f:
        f.write(clean_bytes)
    print("Script1.js sanitized and saved as pure UTF-8!")
except Exception as e:
    print(e)
