from luck360_mcp_server import calc_all_patterns

res = calc_all_patterns('398', '90K 10398')
print('Base: 398 -> Target Result: 500')
for k, v in res.items():
    val = v['val']
    is_straight = (val == '500')
    is_box = (sorted(val) == sorted('500'))
    note = " ★★★ STRAIGHT HIT!" if is_straight else (" ★★ BOX HIT!" if is_box else "")
    print(f"  {k}: {val} {note}")
