import io
import re
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
target = r"            renderCrossSlotPatternTab\(\);\n          \}"
replacement = r"            renderCrossSlotPatternTab();\n            if (typeof renderUpcomingSchedule === 'function') renderUpcomingSchedule();\n          }"
content = re.sub(target, replacement, content)
with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
print("Injected renderUpcomingSchedule into pollLiveDatabase")
