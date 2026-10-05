import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "Populate TOP 7 RULES" in content:
    print("Found Populate TOP 7 RULES in script1.js")
else:
    print("NOT FOUND")
