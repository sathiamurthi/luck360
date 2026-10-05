import io
content = io.open('debug.js', 'r', encoding='utf-8').read()
idx = content.find("Cross-Day Generated Targets")
if idx != -1:
    print("Found Cross-Day Generated Targets in debug.js!")
else:
    print("NOT FOUND in debug.js")
