import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("renderCrossSlotPatternTab();")
if idx != -1:
    print(f"Found call at {idx}")
    print(content[idx:idx+100])
else:
    print("Call not found")
