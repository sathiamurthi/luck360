import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("renderCrossSlotPatternTab();")
print(f"Call is at {idx}")
idx2 = content.find("function renderCrossSlotPatternTab")
print(f"Def is at {idx2}")
