import sys
sys.path.insert(0, '.')
from report_analytics import calc_all_patterns
from luck360_mcp_server import calc_blind_tweak_patterns

sys.stdout.reconfigure(encoding='utf-8')

head_8pm = '944' # First 3 digits of 94406
tail_8pm = '406' # Last 3 digits of 94406

print("=== PATTERNS ON HEAD 3 (944) OF 8 PM ===")
p_head = calc_all_patterns(head_8pm)
for k, v in p_head.items():
    val = v['val']
    print(f"{k:20}: {val} (AB: {val[:2]}) - {v.get('label', '')}")

print("\n=== PATTERNS ON TAIL 3 (406) OF 8 PM ===")
p_tail = calc_all_patterns(tail_8pm)
for k, v in p_tail.items():
    val = v['val']
    print(f"{k:20}: {val} (AB: {val[:2]}) - {v.get('label', '')}")

print("\n=== BLIND TWEAKS ON HEAD 3 (944) ===")
b_head = calc_blind_tweak_patterns(head_8pm)['blind_patterns']
for k, v in b_head.items():
    print(f"{k:22}: {v['target']} (AB: {v['pairs']['AB']}) - {v.get('name', '')}")

print("\n=== BLIND TWEAKS ON TAIL 3 (406) ===")
b_tail = calc_blind_tweak_patterns(tail_8pm)['blind_patterns']
for k, v in b_tail.items():
    print(f"{k:22}: {v['target']} (AB: {v['pairs']['AB']}) - {v.get('name', '')}")
