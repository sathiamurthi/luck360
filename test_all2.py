import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("function renderCrossSlotPatternTab")
print(content[idx:idx+500])
