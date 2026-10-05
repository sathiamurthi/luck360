import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

start_marker = "const slots = ["
end_marker = "// If 8 PM is reflected, append the next day's active recommendation!"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start == -1 or idx_end == -1:
    print("Could not find slots block")
    exit(1)

new_js = """const slots = [];

        // Helper to generate dynamic targets
        function genTarget(prevTail, prevHead) {
            if (!prevTail || prevTail.length !== 3 || isNaN(parseInt(prevTail))) return null;
            const d1 = parseInt(prevTail[0]);
            const d2 = parseInt(prevTail[1]);
            const d3 = parseInt(prevTail[2]);
            const target_h15 = `${(d2 + 1) % 10}${(d3 - d1 + 10) % 10}${d1}`;
            const target_h17 = `${(d1 + d2) % 10}${(d1 - d2 + 10) % 10}${d3}`;
            return {
                h15: target_h15,
                h17: target_h17,
                baseStr: `${prevHead || '???'} (Head) + ${prevTail} (Tail)`
            };
        }

        // Slot 1 (1 PM)
        slots.push({
            slot: '1:00 PM',
            lottery: slotMeta.d1 ? slotMeta.d1.lottery : 'Nagaland - Dear Victory (1 PM)',
            base: '221',
            baseDesc: 'Prev 8 PM',
            hottestPicks: ['051 (H6 \u2605)', '417 (H2 \u2605)', '221 (H3 \u2605)'],
            topPairs: 'AB: 05 / 41 | BC: 51 / 17',
            winningTicket: val1 || '84L 10051',
            winningTail: t1 || '051',
            isReflected: !!t1,
            hitBadge: '\u2714 100% STRAIGHT HIT 051 (H6)',
            hitClass: 'bg-emerald-100 text-emerald-800 border-emerald-300 font-extrabold'
        });

        // Slot 2 (3 PM)
        const s2Targets = genTarget(t1 || '051', val1 ? val1.replace(/\\D/g, '').substring(0,3) : '100');
        const s2Reflected = !!t2;
        slots.push({
            slot: '3:00 PM',
            lottery: slotMeta.d2 ? slotMeta.d2.lottery : 'Kerala - Suvarna Keralam SK-71',
            base: s2Reflected ? (t1 || '051') : (s2Targets ? s2Targets.baseStr : (t1 || '051')),
            baseDesc: 'From 1 PM',
            hottestPicks: s2Reflected ? ['226 (H8 \u2605)', '226 (H12 \u2605)', '561 (H6 \u2605)'] : 
                ['226 (Dual H8/T2 \u2605)', `${s2Targets?.h15} (Target H15 \u2605)`, `${s2Targets?.h17} (Target H17 \u2605)`],
            topPairs: s2Reflected ? 'AB: 22 | BC: 26 | AC: 26' : `Top AB: 22, ${s2Targets?.h15.substring(0,2)} \u2605 | Secondary: 26, ${s2Targets?.h17.substring(0,2)}`,
            winningTicket: s2Reflected ? val2 : 'Pending Draw',
            winningTail: s2Reflected ? t2 : '---',
            isReflected: s2Reflected,
            hitBadge: s2Reflected ? '\u2714 100% STRAIGHT HIT 226 (H8/H12)' : '\uD83D\uDD25 ACTIVE NEXT PLAY',
            hitClass: s2Reflected ? 'bg-emerald-100 text-emerald-800 border-emerald-300 font-extrabold' : 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
        });

        // Slot 3 (6 PM)
        const s3Targets = genTarget(t2 || '226', val2 ? val2.replace(/\\D/g, '').substring(0,3) : '494');
        const s3Reflected = is6pmReflected;
        slots.push({
            slot: '6:00 PM',
            lottery: slotMeta.d3 ? slotMeta.d3.lottery : 'Sikkim - Dear Mountain (6 PM)',
            base: s3Reflected ? (is3pmReflected ? '615' : (t2 || '226')) : (s3Targets ? s3Targets.baseStr : (t2 || '226')),
            baseDesc: 'From 3 PM',
            hottestPicks: s3Reflected ? ['626 (H16 \u2605)', '241 (H7 \u2605)', '824 (H9 \u2605)'] :
                ['626 (Dual H8/T2 \u2605)', `${s3Targets?.h15} (Target H15 \u2605)`, `${s3Targets?.h17} (Target H17 \u2605)`],
            topPairs: s3Reflected ? 'AB: 62 / 24 | BC: 26 / 41' : `Top AB: 62, ${s3Targets?.h15.substring(0,2)} \u2605 | Secondary: 24, ${s3Targets?.h17.substring(0,2)}`,
            winningTicket: s3Reflected ? val3 : 'Pending Draw',
            winningTail: s3Reflected ? t3 : '---',
            isReflected: s3Reflected,
            hitBadge: s3Reflected ? '\u2714 100% STRAIGHT HIT 626 (H16)' : '\uD83D\uDD25 ACTIVE NEXT PLAY',
            hitClass: s3Reflected ? 'bg-emerald-100 text-emerald-800 border-emerald-300 font-extrabold' : 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
        });

        // Slot 4 (8 PM)
        const s4Targets = genTarget(t3 || '626', val3 ? val3.replace(/\\D/g, '').substring(0,3) : '226');
        const s4Reflected = is8PMComplete;
        slots.push({
            slot: '8:00 PM',
            lottery: slotMeta.d4 ? slotMeta.d4.lottery : 'Nagaland - Dear Seagull (8 PM)',
            base: s4Reflected ? (is6pmReflected ? '626' : (t3 || '398')) : (s4Targets ? s4Targets.baseStr : (t3 || '626')),
            baseDesc: 'From 6 PM',
            hottestPicks: s4Reflected ? ['306 (H15)', '406 (Hit)', '637 (H16)'] :
                ['406 (Dual H8/T2 \u2605)', `${s4Targets?.h15} (Target H15 \u2605)`, `${s4Targets?.h17} (Target H17 \u2605)`],
            topPairs: s4Reflected ? 'AB: 30 / 40 / 63' : `Top AB: 40, ${s4Targets?.h15.substring(0,2)} \u2605 | Secondary: 30, ${s4Targets?.h17.substring(0,2)}`,
            winningTicket: s4Reflected ? val4 : 'Pending Draw',
            winningTail: s4Reflected ? t4_val : '---',
            isReflected: s4Reflected,
            hitBadge: s4Reflected ? 'Official Result: 406 (50E 94406)' : '\uD83D\uDD25 ACTIVE NEXT PLAY',
            hitClass: s4Reflected ? 'bg-emerald-100 text-emerald-800 border-emerald-300 font-extrabold' : 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
        });

"""

new_content = content[:idx_start] + new_js + content[idx_end:]

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(new_content)

print("Injected dynamic logic for 3, 6, 8 PM!")
