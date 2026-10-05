import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("renderCrossSlotPatternTab();")
print(content[max(0, idx-200):idx+200])
