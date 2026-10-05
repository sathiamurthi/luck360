import io
import urllib.request

try:
    content = io.open('script1.js', 'r', encoding='utf-8', errors='strict').read()
    print("Script1.js is perfectly strict UTF-8 encoded.")
except Exception as e:
    print("ENCODING ERROR:", e)
