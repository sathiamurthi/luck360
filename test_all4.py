import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("Cross-Day Generated Targets")
if idx != -1:
    print("Found Cross-Day Generated Targets in all_scripts.js!")
else:
    print("NOT FOUND in all_scripts.js")
