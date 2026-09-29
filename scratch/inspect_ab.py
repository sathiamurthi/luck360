import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/rendered_dom_ab.html', 'r', encoding='utf-8') as f:
    dom = f.read()

print('DOM length:', len(dom))

# 1. Check container-top-ab-pattern6
ab_cards = re.search(r'id="container-top-ab-pattern6"[^>]*>(.*?)</div>\s*<!-- Top 6 AB', dom, re.DOTALL)
if ab_cards:
    content = ab_cards.group(1).strip()
    print('container-top-ab-pattern6 cards length:', len(content))
    pairs = re.findall(r'<div class="text-3xl font-black tracking-widest text-indigo-950 font-mono">(.*?)</div>', content)
    targets = re.findall(r'<div class="text-2xl font-black font-mono text-emerald-700">(.*?)</div>', content)
    print('Rendered Top 6 AB Pairs:', pairs)
    print('Rendered Native Targets:', targets)
else:
    print('container-top-ab-pattern6 NOT FOUND')

# 2. Check table-top-ab-pattern6
tbody = re.search(r'id="table-top-ab-pattern6"[^>]*>(.*?)</tbody>', dom, re.DOTALL)
if tbody:
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), re.DOTALL)
    print('Top 6 AB Table rows:', len(rows))
    for r in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        clean_tds = [re.sub(r'<[^>]+>', ' ', td).strip() for td in tds]
        print('  Row:', clean_tds[0], '| Seed:', clean_tds[1], '| Native C:', clean_tds[2], '| Prods:', clean_tds[3], '| Diff:', clean_tds[4], '| Sum:', clean_tds[5])
else:
    print('table-top-ab-pattern6 NOT FOUND')
