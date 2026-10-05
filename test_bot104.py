import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "input-draw1" in content:
    print("Found input-draw1")
else:
    print("Missing input-draw1")
