import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""        // If 8 PM is reflected, append the next day's active recommendation!
        if \(is8PMComplete\) \{
          slots\.push\(\{
            slot: 'Tomorrow 1 PM',
            lottery: 'Nagaland State Lottery \(Dear Day\)',
            base: `\$\{h4\} \(Head\) \+ \$\{t4_val\} \(Tail\)`,
            baseDesc: `From 8 PM 50E 94406 \(Head: \$\{h4\}, Tail: \$\{t4_val\}\)`,
            hottestPicks: \['445 \(Dual H8/T2 \)', '559 \(Head H15 \)', '417 \(Tail H16 \)'\],
            topPairs: 'Top AB: 44  \| Secondary: 55, 41',
            winningTicket: 'Pending Draw',
            winningTail: '---',
            isReflected: false,
            hitBadge: ' ACTIVE NEXT PLAY',
            hitClass: 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
          \}\);
        \}"""

new_code = r"""        // If 8 PM is reflected, append the next day's active recommendation!
        if (is8PMComplete) {
          const t4_d1 = parseInt(t4_val[0]);
          const t4_d2 = parseInt(t4_val[1]);
          const t4_d3 = parseInt(t4_val[2]);
          
          const target_h15 = `${(t4_d2 + 1) % 10}${(t4_d3 - t4_d1 + 10) % 10}${t4_d1}`;
          const target_h17 = `${(t4_d1 + t4_d2) % 10}${(t4_d1 - t4_d2 + 10) % 10}${t4_d3}`;
          
          slots.push({
            slot: 'Tomorrow 1 PM',
            lottery: 'Nagaland State Lottery (Dear Day)',
            base: `${h4} (Head) + ${t4_val} (Tail)`,
            baseDesc: `From 8 PM 50E 94406 (Head: ${h4}, Tail: ${t4_val})`,
            hottestPicks: ['445 (Dual H8/T2 \u2605)', '559 (Head H15 \u2605)', '417 (Tail H16 \u2605)', `${target_h15} (Target H15 \u2605)`, `${target_h17} (Target H17 \u2605)`],
            topPairs: `Top AB: 44, ${target_h15.substring(0,2)} \u2605 | Secondary: 55, 41, ${target_h17.substring(0,2)}`,
            winningTicket: 'Pending Draw',
            winningTail: '---',
            isReflected: false,
            hitBadge: ' \uD83D\uDD25 ACTIVE NEXT PLAY',
            hitClass: 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
          });
        }"""

if "slots.push({" in content and "Tomorrow 1 PM" in content:
    content = re.sub(target, lambda m: new_code, content)
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected H15 and H17 patterns into Tomorrow 1 PM block!")
else:
    print("Could not find the block in script1.js")
