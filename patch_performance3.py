import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""      // 4\. TODAY'S PATTERN PERFORMANCE BREAKDOWN
      const todayGrid = document\.getElementById\('report-today-draws-grid'\);
      if \(todayGrid\) \{
        let dynamicBreakdown = \[\];
        if \(typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords\.length > 0\) \{
            const latestDate = drawHistoryRecords\[drawHistoryRecords\.length - 1\]\.date;
            const latestDraws = drawHistoryRecords\.filter\(d => d\.date === latestDate\);
            
            latestDraws\.forEach\(draw => \{
                const prevIdx = drawHistoryRecords\.findIndex\(d => d\.id === draw\.id\) - 1;
                const prevDraw = prevIdx >= 0 \? drawHistoryRecords\[prevIdx\] : null;
                const baseTail = prevDraw \? prevDraw\.tail : '000';
                const baseSlot = prevDraw \? `\$\{prevDraw\.time\} \(\$\{prevDraw\.date === latestDate \? 'Today' : 'Yesterday'\}\)` : 'Unknown Base';
                
                let pats = \{ h15_val: '---', h17_val: '---', h16_val: '---', h8_val: '---', h9_val: '---', h7_val: '---' \};
                let blind = \{ b2: '---', b4: '---', b1: '---' \};
                try \{
                    pats = calculateSingleDrawPatterns\(baseTail\);
                    blind = calcBlindPatterns\(baseTail\);
                \} catch\(e\) \{\}
                
                let winningPattern = 'No Direct 3-Digit Match';
                let formula = 'Derived via secondary pairs';
                let mathProof = 'Top pairs hit in AB/BC/AC slots';
                let matchType = 'SECONDARY MATCH';
                let sig = 'Top pairs mathematically hit but not exact 3-digit order.';
                
                if \(draw\.tail === pats\.h15_val\) \{ winningPattern = 'Star H15'; formula = '\(D2\+1, D3-D1, D1\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                else if \(draw\.tail === pats\.h17_val\) \{ winningPattern = 'Star H17'; formula = '\(D1\+D2, D1-D2, D3\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                else if \(draw\.tail === pats\.h16_val\) \{ winningPattern = 'Pattern H16'; formula = '\(D1, D2\+1, D3\+1\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                else if \(draw\.tail === pats\.h8_val\) \{ winningPattern = 'Star H8'; formula = '\(D1\+D3\+1, D1\+D3\+1, D2\+1\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                else if \(draw\.tail === blind\.b2\) \{ winningPattern = 'Tail Blind T2'; formula = '\(D1\+D2, D1, D3-1\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                else if \(draw\.tail === blind\.b4\) \{ winningPattern = 'Head Blind T4'; formula = '\(D1-D3, D1-D3, D3-2\)'; mathProof = `Matched Base \$\{baseTail\}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; \}
                
                dynamicBreakdown\.push\(\{
                    slot: draw\.time,
                    lottery: draw\.company,
                    match_type: matchType,
                    ticket: draw\.ticket,
                    winning_tail: draw\.tail,
                    base_tail: baseTail,
                    derived_from_slot: baseSlot,
                    winning_pattern: winningPattern,
                    formula: formula,
                    math_proof: mathProof,
                    significance: sig
                \}\);
            \}\);
        \}"""

replacement = """      // 4. TODAY'S PATTERN PERFORMANCE BREAKDOWN
      const todayGrid = document.getElementById('report-today-draws-grid');
      if (todayGrid) {
        let dynamicBreakdown = [];
        if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length > 0) {
            const latestDate = drawHistoryRecords[drawHistoryRecords.length - 1].date;
            const latestDraws = drawHistoryRecords.filter(d => d.date === latestDate);
            
            latestDraws.forEach(draw => {
                const prevIdx = drawHistoryRecords.findIndex(d => d.id === draw.id) - 1;
                const prevDraw = prevIdx >= 0 ? drawHistoryRecords[prevIdx] : null;
                const prevTicket = prevDraw ? prevDraw.ticket : '50E 94406';
                const baseExtracted = extractHeadAndTail(prevTicket);
                const baseTail = baseExtracted.tail;
                const baseHead = baseExtracted.head;
                const baseSlot = prevDraw ? `${prevDraw.time} (${prevDraw.date === latestDate ? 'Today' : 'Yesterday'})` : 'Unknown Base';
                
                let tailPats = {}, headPats = {}, blind = {};
                try {
                    tailPats = calculateSingleDrawPatterns(baseTail);
                    headPats = calculateSingleDrawPatterns(baseHead);
                    blind = calcBlindPatterns(baseTail);
                } catch(e) {}
                
                const targets = [
                    { name: 'Tail H15', val: tailPats.h15_val },
                    { name: 'Tail H17', val: tailPats.h17_val },
                    { name: 'Head H15', val: headPats.h15_val },
                    { name: 'Head H17', val: headPats.h17_val },
                    { name: 'Tail H16', val: tailPats.h16_val },
                    { name: 'Tail H9', val: tailPats.h9_val },
                    { name: 'Tail H8', val: tailPats.h8_val },
                    { name: 'Tail Blind T2', val: blind.b2 }
                ];
                
                let winningPattern = 'No Direct Match';
                let formula = 'Evaluating pairs...';
                let mathProof = '';
                let matchType = 'SECONDARY PAIR MATCH';
                let sig = 'Secondary pair locked.';
                
                // Check straight hit
                let straightHit = targets.find(t => t.val === draw.tail);
                if (straightHit) {
                    winningPattern = straightHit.name;
                    formula = 'Perfect 3-Digit Alignment';
                    mathProof = `${straightHit.name} -> ${straightHit.val}`;
                    matchType = 'STRAIGHT HIT';
                    sig = 'Perfect straight 3-digit algorithmic lock!';
                } else {
                    // Check pairs
                    const AB = draw.tail.substring(0,2);
                    const BC = draw.tail.substring(1,3);
                    let pairsHit = [];
                    targets.forEach(t => {
                        if (t.val && t.val.substring(0,2) === AB && !pairsHit.includes(`AB ${AB} from ${t.name}(${t.val})`)) pairsHit.push(`AB ${AB} from ${t.name}(${t.val})`);
                        if (t.val && t.val.substring(1,3) === BC && !pairsHit.includes(`BC ${BC} from ${t.name}(${t.val})`)) pairsHit.push(`BC ${BC} from ${t.name}(${t.val})`);
                    });
                    if (pairsHit.length > 0) {
                        winningPattern = 'Pair Confluence';
                        formula = 'Partial Alignment';
                        mathProof = pairsHit.join(' | ');
                    } else {
                        mathProof = `Tail H15: ${tailPats.h15_val}, Head H17: ${headPats.h17_val}`;
                        sig = 'No mathematical correlation found in primary targets.';
                    }
                }
                
                dynamicBreakdown.push({
                    slot: draw.time,
                    lottery: draw.company,
                    match_type: matchType,
                    ticket: draw.ticket,
                    winning_tail: draw.tail,
                    base_tail: baseTail,
                    derived_from_slot: baseSlot,
                    winning_pattern: winningPattern,
                    formula: formula,
                    math_proof: mathProof,
                    significance: sig
                });
            });
            
            // GENERATE PENDING NEXT DRAW
            const lastDraw = latestDraws[latestDraws.length - 1];
            let nextSlot = 'Unknown';
            if (lastDraw.time.includes('1:00 PM')) nextSlot = '3:00 PM';
            else if (lastDraw.time.includes('3:00 PM')) nextSlot = '6:00 PM';
            else if (lastDraw.time.includes('6:00 PM')) nextSlot = '8:00 PM';
            else if (lastDraw.time.includes('8:00 PM')) nextSlot = '1:00 PM (Tomorrow)';
            
            const pExt = extractHeadAndTail(lastDraw.ticket);
            let tPats = {h17_val:'---', h15_val:'---'}, hPats = {h17_val:'---', h15_val:'---'};
            try {
                tPats = calculateSingleDrawPatterns(pExt.tail);
                hPats = calculateSingleDrawPatterns(pExt.head);
            } catch(e) {}
            
            dynamicBreakdown.push({
                slot: nextSlot,
                lottery: 'PENDING PREDICTION',
                match_type: 'AWAITING RESULT',
                ticket: 'PENDING',
                winning_tail: '???',
                base_tail: pExt.tail,
                derived_from_slot: `${lastDraw.time} (Latest)`,
                winning_pattern: 'Target Projections',
                formula: 'H15 & H17 Math',
                math_proof: `Tail H17: ${tPats.h17_val} | Tail H15: ${tPats.h15_val} | Head H17: ${hPats.h17_val} | Head H15: ${hPats.h15_val}`,
                significance: `Top pairs to watch: ${tPats.h17_val.substring(0,2)}, ${hPats.h17_val.substring(0,2)}, ${tPats.h15_val.substring(0,2)}`
            });
        }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched Today's Analysis logic successfully.")
else:
    print("Target block not found.")
