import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "function renderCrossSlotPatternTab" in content:
    print("Found in script1")
else:
    print("NOT in script1")
