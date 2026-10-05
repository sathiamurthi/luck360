# -*- coding: utf-8 -*-
import io
import re

content = io.open('index - Copy.html', 'r', encoding='utf-8').read()

# 1. Add box-active-baseline
idx_box = content.find('<section id="container-cross-consensus"')
if idx_box != -1 and "box-active-baseline" not in content:
    content = content[:idx_box] + '<div id="box-active-baseline" class="mb-6"></div>\n      ' + content[idx_box:]

# 2. Fix the header and table body for Dynamic Schedule
new_header = '<span id="schedule-header-title"><span>??</span> Dynamic Daily Guess Schedule</span>'
content = re.sub(r'<span>.*?</span> Today \(25-Sep\) &amp; Upcoming Guess Schedule', new_header, content)
content = re.sub(r'<span>.*?</span> Today \(25-Sep\) & Upcoming Guess Schedule', new_header, content)

new_badge = '<span id="schedule-header-badge" class="px-3 py-1 rounded-full text-xs font-mono font-bold border border-emerald-300 bg-emerald-50 text-emerald-800">Live Updating</span>'
content = content.replace('<span class="px-3 py-1 rounded-full text-xs font-mono font-bold border border-emerald-300 bg-emerald-50 text-emerald-800">25-Sep to 30-Sep</span>', new_badge)

target_table = r'<tbody class="divide-y divide-slate-200 text-xs font-medium text-slate-800">\s*<tr.*?</tr>\s*<tr.*?</tr>\s*<tr.*?</tr>\s*</tbody>'
new_table = r'<tbody id="tbody-upcoming-schedule" class="divide-y divide-slate-200 text-xs font-medium text-slate-800"></tbody>'
content = re.sub(target_table, new_table, content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully restored index.html and applied fixes!")
