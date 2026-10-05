import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("function renderCrossSlotPatternTab")
div_start = content.rfind('function', 0, idx)
print(content[div_start-200:div_start+100])
