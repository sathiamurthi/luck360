import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("function renderCrossSlotPatternTab")
if idx != -1:
    print("Found renderCrossSlotPatternTab in all_scripts.js!")
else:
    print("NOT FOUND in all_scripts.js")
