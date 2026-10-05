import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()

# Replace header using regex that ignores the exact emoji bytes
content = re.sub(r'<span>.*?</span> Today \(25-Sep\) & Upcoming Guess Schedule', r'<span id="schedule-header-title"><span>\U0001f52e</span> Dynamic Daily Guess Schedule</span>', content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated header!")
