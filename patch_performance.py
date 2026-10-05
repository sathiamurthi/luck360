import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""      // 4. TODAY'S PATTERN PERFORMANCE BREAKDOWN
      const todayGrid = document.getElementById\('report-today-draws-grid'\);
      if \(todayGrid && report\.current_day_analysis\) \{
        todayGrid\.innerHTML = report\.current_day_analysis\.draw_breakdown\.map\(draw => `
          <div class="theme-card-inner border rounded-xl p-4 space-y-2 font-mono text-xs shadow-sm bg-white border-slate-300">
            <div class="flex justify-between items-center border-b border-slate-200 pb-2">
              <div class="flex items-center gap-2">
                <span class="font-extrabold text-slate-900 text-sm">\$\{draw\.slot\}</span>
                <span class="text-\[10px\] text-slate-600 font-sans font-medium">\$\{draw\.lottery\}</span>
              </div>
              <span class="px-2\.5 py-0\.5 rounded-full text-\[10px\] font-black border bg-emerald-100 text-emerald-900 border-emerald-300">\$\{draw\.match_type\}</span>
            </div>

            <div class="grid grid-cols-2 gap-2 text-\[11px\] pt-1">
              <div>
                <span class="text-slate-500 font-sans">Winning Result:</span><br>
                <strong class="font-mono text-slate-900 text-sm font-black">\$\{draw\.ticket\} \(\$\{draw\.winning_tail\}\)</strong>
              </div>
              <div>
                <span class="text-slate-500 font-sans">Derived From Base:</span><br>
                <strong class="font-mono text-indigo-900 text-sm font-black">\$\{draw\.base_tail\}</strong> <span class="text-\[10px\] text-slate-500 font-sans">\(\$\{draw\.derived_from_slot\.split\('\('\)\[0\]\}\)</span>
              </div>
            </div>

            <div class="bg-slate-50 p-2\.5 rounded-lg border border-slate-200 space-y-1 text-\[11px\]">
              <div><span class="font-bold text-slate-700">Winning Pattern:</span> <strong class="text-emerald-800 font-black">\$\{draw\.winning_pattern\}</strong></div>
              <div><span class="font-bold text-slate-700">Formula Rule:</span> <span class="text-indigo-800 font-mono">\$\{draw\.formula\}</span></div>
              <div><span class="font-bold text-slate-700">Arithmetic Proof:</span> <span class="text-emerald-700 font-mono font-bold">\$\{draw\.math_proof\}</span></div>
            </div>

            <div class="text-\[10px\] text-slate-600 font-sans font-medium leading-tight">
              \$\{draw\.significance\}
            </div>
          </div>
        `\)\.join\(''\);
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
                const baseTail = prevDraw ? prevDraw.tail : '000';
                const baseSlot = prevDraw ? `${prevDraw.time} (${prevDraw.date === latestDate ? 'Today' : 'Yesterday'})` : 'Unknown Base';
                
                let pats = { h15_val: '---', h17_val: '---', h16_val: '---', h8_val: '---', h9_val: '---', h7_val: '---' };
                let blind = { b2: '---', b4: '---', b1: '---' };
                try {
                    pats = calculateSingleDrawPatterns(baseTail);
                    blind = calcBlindPatterns(baseTail);
                } catch(e) {}
                
                let winningPattern = 'No Direct 3-Digit Match';
                let formula = 'Derived via secondary pairs';
                let mathProof = 'Top pairs hit in AB/BC/AC slots';
                let matchType = 'SECONDARY MATCH';
                let sig = 'Top pairs mathematically hit but not exact 3-digit order.';
                
                if (draw.tail === pats.h15_val) { winningPattern = 'Star H15'; formula = '(D2+1, D3-D1, D1)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                else if (draw.tail === pats.h17_val) { winningPattern = 'Star H17'; formula = '(D1+D2, D1-D2, D3)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                else if (draw.tail === pats.h16_val) { winningPattern = 'Pattern H16'; formula = '(D1, D2+1, D3+1)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                else if (draw.tail === pats.h8_val) { winningPattern = 'Star H8'; formula = '(D1+D3+1, D1+D3+1, D2+1)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                else if (draw.tail === blind.b2) { winningPattern = 'Tail Blind T2'; formula = '(D1+D2, D1, D3-1)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                else if (draw.tail === blind.b4) { winningPattern = 'Head Blind T4'; formula = '(D1-D3, D1-D3, D3-2)'; mathProof = `Matched Base ${baseTail}`; matchType = 'STRAIGHT HIT'; sig = 'Perfect straight 3-digit algorithmic lock!'; }
                
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
        }
        
        const dataToRender = dynamicBreakdown.length > 0 ? dynamicBreakdown : (report && report.current_day_analysis ? report.current_day_analysis.draw_breakdown : []);
        
        todayGrid.innerHTML = dataToRender.map(draw => `
          <div class="theme-card-inner border rounded-xl p-4 space-y-2 font-mono text-xs shadow-sm bg-white border-slate-300">
            <div class="flex justify-between items-center border-b border-slate-200 pb-2">
              <div class="flex items-center gap-2">
                <span class="font-extrabold text-slate-900 text-sm">${draw.slot}</span>
                <span class="text-[10px] text-slate-600 font-sans font-medium">${draw.lottery}</span>
              </div>
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black border bg-emerald-100 text-emerald-900 border-emerald-300">${draw.match_type}</span>
            </div>

            <div class="grid grid-cols-2 gap-2 text-[11px] pt-1">
              <div>
                <span class="text-slate-500 font-sans">Winning Result:</span><br>
                <strong class="font-mono text-slate-900 text-sm font-black">${draw.ticket} (${draw.winning_tail})</strong>
              </div>
              <div>
                <span class="text-slate-500 font-sans">Derived From Base:</span><br>
                <strong class="font-mono text-indigo-900 text-sm font-black">${draw.base_tail}</strong> <span class="text-[10px] text-slate-500 font-sans">(${draw.derived_from_slot.split('(')[0]})</span>
              </div>
            </div>

            <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-200 space-y-1 text-[11px]">
              <div><span class="font-bold text-slate-700">Winning Pattern:</span> <strong class="text-emerald-800 font-black">${draw.winning_pattern}</strong></div>
              <div><span class="font-bold text-slate-700">Formula Rule:</span> <span class="text-indigo-800 font-mono">${draw.formula}</span></div>
              <div><span class="font-bold text-slate-700">Arithmetic Proof:</span> <span class="text-emerald-700 font-mono font-bold">${draw.math_proof}</span></div>
            </div>

            <div class="text-[10px] text-slate-600 font-sans font-medium leading-tight">
              ${draw.significance}
            </div>
          </div>
        `).join('');
      }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Injected dynamic logic for Today's Pattern Performance")
else:
    print("Could not find the target section for Today's Pattern Performance")
