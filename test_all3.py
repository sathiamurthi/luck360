import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("// Populate TOP 7 RULES")
if idx != -1:
    print(f"Found // Populate TOP 7 RULES at {idx}")
else:
    print("Not found")
