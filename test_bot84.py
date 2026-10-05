import js2py
import io

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
try:
    # Just parse it using a simple method if js2py works, else we just use a small custom regex
    pass
except Exception as e:
    print(e)
print("done")
