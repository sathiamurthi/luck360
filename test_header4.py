import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()

new_header = '<span id="schedule-header-title"><span>\uD83D\uDD2E</span> Dynamic Daily Guess Schedule</span>'
content = re.sub(r'<span>.*?</span> Today \(25-Sep\) & Upcoming Guess Schedule', lambda m: new_header, content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated header!")
