import sys
sys.path.insert(0, '.')
import report_analytics, json

sys.stdout.reconfigure(encoding='utf-8')

rep = report_analytics.generate_comprehensive_report()
print(f"Total enriched draws: {len(rep['enriched_draw_history'])}")
for item in rep['enriched_draw_history'][-4:]:
    print('-------------------------')
    print(f"{item['date']} {item['time']} | Tail: {item['tail']} | AB: {item.get('ab_pair')} ({item.get('ab_frequency_desc')})")
    print('  Winning 3-Digit Patterns:', [w['name'] + ' (' + w['type'] + ') from ' + w['source'] for w in item.get('winning_patterns', [])])
    print('  Winning AB Patterns:', [ab['name'] + ' -> ' + ab['pair'] for ab in item.get('winning_ab_patterns', [])])
