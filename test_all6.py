import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
if "top 7" in content.lower():
    print("Found top 7 in all_scripts.js")
else:
    print("Not found")
