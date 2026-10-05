import re

with open('script1.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the hardcoded 406 fallback
fallback_logic = '''
                if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length > 0) {
                    const sorted = drawHistoryRecords.filter(r => /^\\\d{3}$/.test(r.tail)).sort((a,b) => new Date(a.date) - new Date(b.date));
                    const latestDate = sorted[sorted.length-1].date;
                    const prev = sorted.filter(r => r.date !== latestDate);
                    if (prev.length > 0) {
                        tailA = prev[prev.length-1].tail;
                    } else {
                        tailA = '406';
                    }
                } else {
                    tailA = '406';
                }
'''
content = re.sub(
    r"tailA = '406'; // Prev day fallback",
    fallback_logic.strip(),
    content
)

# Fix active tabs
content = re.sub(
    r"(deactivateAllTabs\(\);\s*\n\s*(\w+Btn)\.classList\.add\('active-tab'\);)",
    r"\1\n      \2.classList.remove('text-slate-600');\n      \2.classList.add('text-slate-900');",
    content
)

content = re.sub(
    r"(b\.classList\.add\('text-slate-600'\);)",
    r"\1\n          b.classList.remove('text-slate-900');",
    content
)

with open('script1.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('script1.js updated.')