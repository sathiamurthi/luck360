import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/rendered_dom.html', 'r', encoding='utf-8') as f:
    dom = f.read()

print('Rendered DOM length:', len(dom))

m4 = re.search(r'id="container-4draw-matrix"[^>]*>(.*?)</div>\s*<!-- Official', dom, re.DOTALL)
if m4:
    content = m4.group(1).strip()
    print('container-4draw-matrix length:', len(content))
    slots = re.findall(r'<span class="text-xs font-black[^>]*>(.*?)</span>', content)
    print('Slots in matrix:', slots)
    tickets = re.findall(r'<div class="text-sm font-black text-slate-900 font-mono mt-0.5 truncate">(.*?)</div>', content)
    print('Tickets in matrix:', tickets)

tbody = re.search(r'id="table-official-draw-results"[^>]*>(.*?)</tbody>', dom, re.DOTALL)
if tbody:
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), re.DOTALL)
    print('Audit table rows:', len(rows))
    for r in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        clean_tds = [re.sub(r'<[^>]+>', ' ', td).strip() for td in tds]
        print('  Row:', clean_tds[:4])

banner = re.search(r'id="banner-hottest-recommendations"[^>]*>(.*?)</div>\s*<div', dom, re.DOTALL)
if banner:
    print('Banner:', re.sub(r'<[^>]+>', ' ', banner.group(1)).strip()[:150])

hot_picks = re.search(r'id="container-hot-from-each-pattern"[^>]*>(.*?)</div>\s*<!-- 3-COL', dom, re.DOTALL)
if hot_picks:
    print('Hot from each pattern length:', len(hot_picks.group(1).strip()))
    cards = re.findall(r'<span class="text-2xl font-black font-mono tracking-widest text-slate-900">(.*?)</span>', hot_picks.group(1))
    print('Hot picks numbers:', cards)

for i in range(1, 5):
    m = re.search(r'id="input-draw' + str(i) + r'"[^>]*value="([^"]*)"', dom)
    val = m.group(1) if m else 'NOT FOUND'
    print(f'input-draw{i} HTML value attr: {val}')
