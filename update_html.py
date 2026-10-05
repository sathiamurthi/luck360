import io
import re

content = io.open('index.html', 'r', encoding='utf-8').read()

target_header = r'<span>\U0001f52e</span> Today \(25-Sep\) &amp; Upcoming Guess Schedule'
target_header2 = r'<span>\U0001f52e</span> Today \(25-Sep\) & Upcoming Guess Schedule'

new_header = r'<span id="schedule-header-title"><span>\U0001f52e</span> Dynamic Daily Guess Schedule</span>'
content = content.replace('<span>\U0001f52e</span> Today (25-Sep) & Upcoming Guess Schedule', new_header)
content = content.replace('<span>\U0001f52e</span> Today (25-Sep) &amp; Upcoming Guess Schedule', new_header)

target_badge = r'<span class="px-3 py-1 rounded-full text-xs font-mono font-bold border border-emerald-300 bg-emerald-50 text-emerald-800">25-Sep to 30-Sep</span>'
new_badge = r'<span id="schedule-header-badge" class="px-3 py-1 rounded-full text-xs font-mono font-bold border border-emerald-300 bg-emerald-50 text-emerald-800">Live Updating</span>'
content = content.replace('<span class="px-3 py-1 rounded-full text-xs font-mono font-bold border border-emerald-300 bg-emerald-50 text-emerald-800">25-Sep to 30-Sep</span>', new_badge)

target_table = r'<tbody class="divide-y divide-slate-200 text-xs font-medium text-slate-800">\s*<tr.*?</tr>\s*<tr.*?</tr>\s*<tr.*?</tr>\s*</tbody>'
new_table = r'<tbody id="tbody-upcoming-schedule" class="divide-y divide-slate-200 text-xs font-medium text-slate-800"></tbody>'
content = re.sub(target_table, new_table, content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html headers and table body IDs")
