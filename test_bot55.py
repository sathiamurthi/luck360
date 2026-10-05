import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if 'id="nr-p1"' in content:
    print("Found nr-p1")
else:
    print("Missing nr-p1")
