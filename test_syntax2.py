import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
try:
    import js2py
    js2py.parse_js(content)
    print("Valid syntax!")
except Exception as e:
    print("Syntax error:", e)
