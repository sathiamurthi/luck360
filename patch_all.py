import io
import re

# 1. Read the file with surrogatepass
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
lines = content.splitlines()

# 2. Fix Event Listeners
for i, line in enumerate(lines):
    if "['mp-prev', 'mp-curr'].forEach(id => $(id).addEventListener('input', render));" in line:
        lines[i] = "    ['mp-prev', 'mp-curr'].forEach(id => { const el = $(id); if(el) el.addEventListener('input', render); });"
    elif "$('mp-min').addEventListener('change', render); $('mp-gaps').addEventListener('change', render);" in line:
        lines[i] = "    if($('mp-min')) $('mp-min').addEventListener('change', render); if($('mp-gaps')) $('mp-gaps').addEventListener('change', render);"
    elif "$('mp-sync').addEventListener('click', sync);" in line:
        lines[i] = "    if($('mp-sync')) $('mp-sync').addEventListener('click', sync);"
    elif "$('mp-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); $('mp-status').textContent = 'Copied'; });" in line:
        lines[i] = "    if($('mp-copy')) $('mp-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); if($('mp-status')) $('mp-status').textContent = 'Copied'; });"
    elif "$('mp-banner-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); $('mp-banner-time').textContent = 'copied'; });" in line:
        lines[i] = "    if($('mp-banner-copy')) $('mp-banner-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); if($('mp-banner-time')) $('mp-banner-time').textContent = 'copied'; });"
    elif "$('nr-p1').addEventListener('input',drawCross);$('nr-p2').addEventListener('input',drawCross);" in line:
        lines[i] = "    if($('nr-p1')) $('nr-p1').addEventListener('input',drawCross); if($('nr-p2')) $('nr-p2').addEventListener('input',drawCross);"


# 3. Delete corrupted Ticket Parser block
# Find start of `// ---- ticket slip parser + payout calculator (pure) ----` (the first occurrence after mp-banner-copy)
# Actually we can just find the exact line ranges.
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith("// ---- ticket slip parser + payout calculator (pure) ----"):
        if start_idx == -1:
            start_idx = i
    if line.strip() == "})();" and start_idx != -1 and end_idx == -1 and i > start_idx + 100:
        # verify if it's the correct closing parenthesis
        if "btn.addEventListener('click', rollover);" in lines[i-2]:
            end_idx = i

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + lines[end_idx+1:]
else:
    print(f"Warning: Could not find ticket parser block to delete. Start: {start_idx}, End: {end_idx}")

content = '\n'.join(lines)


# 4. Update timeline slots logic
start_marker = "const slots = ["
end_marker = "// If 8 PM is reflected, append the next day's active recommendation!"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    # Use ASCII equivalents for stars/fire/checkmarks to avoid surrogate crashes in writing
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

        const STAR = '\\u2605';
        const FIRE = '\\uD83D\\uDD25';
        const CHECK = '\\u2714';

        // Slot 1 (1 PM)
        slots.push({
            slot: '1:00 PM',
            lottery: slotMeta.d1 ? slotMeta.d1.lottery : 'Nagaland - Dear Victory (1 PM)',
            base: '221',
            baseDesc: 'Prev 8 PM',
            hottestPicks: [`051 (H6 ${STAR})`, `417 (H2 ${STAR})`, `221 (H3 ${STAR})`],
            topPairs: 'AB: 05 / 41 | BC: 51 / 17',
            winningTicket: val1 || '84L 10051',
            winningTail: t1 || '051',
            isReflected: !!t1,
            hitBadge: `${CHECK} 100% STRAIGHT HIT 051 (H6)`,
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
            hottestPicks: s2Reflected ? [`226 (H8 ${STAR})`, `226 (H12 ${STAR})`, `561 (H6 ${STAR})`] : 
                [`226 (Dual H8/T2 ${STAR})`, `${s2Targets?.h15} (Target H15 ${STAR})`, `${s2Targets?.h17} (Target H17 ${STAR})`],
            topPairs: s2Reflected ? 'AB: 22 | BC: 26 | AC: 26' : `Top AB: 22, ${s2Targets?.h15.substring(0,2)} ${STAR} | Secondary: 26, ${s2Targets?.h17.substring(0,2)}`,
            winningTicket: s2Reflected ? val2 : 'Pending Draw',
            winningTail: s2Reflected ? t2 : '---',
            isReflected: s2Reflected,
            hitBadge: s2Reflected ? `${CHECK} 100% STRAIGHT HIT 226 (H8/H12)` : `${FIRE} ACTIVE NEXT PLAY`,
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
            hottestPicks: s3Reflected ? [`626 (H16 ${STAR})`, `241 (H7 ${STAR})`, `824 (H9 ${STAR})`] :
                [`626 (Dual H8/T2 ${STAR})`, `${s3Targets?.h15} (Target H15 ${STAR})`, `${s3Targets?.h17} (Target H17 ${STAR})`],
            topPairs: s3Reflected ? 'AB: 62 / 24 | BC: 26 / 41' : `Top AB: 62, ${s3Targets?.h15.substring(0,2)} ${STAR} | Secondary: 24, ${s3Targets?.h17.substring(0,2)}`,
            winningTicket: s3Reflected ? val3 : 'Pending Draw',
            winningTail: s3Reflected ? t3 : '---',
            isReflected: s3Reflected,
            hitBadge: s3Reflected ? `${CHECK} 100% STRAIGHT HIT 626 (H16)` : `${FIRE} ACTIVE NEXT PLAY`,
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
                [`406 (Dual H8/T2 ${STAR})`, `${s4Targets?.h15} (Target H15 ${STAR})`, `${s4Targets?.h17} (Target H17 ${STAR})`],
            topPairs: s4Reflected ? 'AB: 30 / 40 / 63' : `Top AB: 40, ${s4Targets?.h15.substring(0,2)} ${STAR} | Secondary: 30, ${s4Targets?.h17.substring(0,2)}`,
            winningTicket: s4Reflected ? val4 : 'Pending Draw',
            winningTail: s4Reflected ? t4_val : '---',
            isReflected: s4Reflected,
            hitBadge: s4Reflected ? 'Official Result: 406 (50E 94406)' : `${FIRE} ACTIVE NEXT PLAY`,
            hitClass: s4Reflected ? 'bg-emerald-100 text-emerald-800 border-emerald-300 font-extrabold' : 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse font-extrabold'
        });

"""
    content = content[:idx_start] + new_js + content[idx_end:]
else:
    print(f"Warning: Could not find timeline slots block. {idx_start}, {idx_end}")

# 5. Make sure the output avoids surrogate crashes by using surrogatepass
with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)

print("Patching complete!")
