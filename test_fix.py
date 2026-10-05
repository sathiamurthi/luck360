import io
content = io.open('script1.js', 'r', encoding='utf-8').read()

# Remove the wrong injection
content = content.replace("            if (typeof renderUpcomingSchedule === 'function') renderUpcomingSchedule();\n", "")

# Find the correct location inside pollLiveDatabase
idx_poll = content.find("calculatePredictions();\n            renderCrossSlotPatternTab();")
if idx_poll != -1:
    div_end = content.find("renderCrossSlotPatternTab();", idx_poll) + len("renderCrossSlotPatternTab();")
    content = content[:div_end] + "\n            if (typeof renderUpcomingSchedule === 'function') renderUpcomingSchedule();" + content[div_end:]
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed injection!")
else:
    print("Not found inside pollLiveDatabase")
