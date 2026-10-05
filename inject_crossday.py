import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Javascript function for Cross-Day logic
js_logic = """
    function getCrossDayPools(history) {
        if (!history || history.length < 2) return null;
        // Find the most recent date with tails
        let validDraws = history.filter(x => x.tail && x.tail.length === 3);
        if (validDraws.length < 2) return null;
        
        let latestDate = validDraws[validDraws.length - 1].date;
        let todaysDraws = validDraws.filter(x => x.date === latestDate);
        
        if (todaysDraws.length < 2) {
            // If only 1 draw today, use previous day as well to get at least 2 draws
            let prevDate = validDraws.filter(x => x.date !== latestDate).pop()?.date;
            todaysDraws = validDraws.filter(x => x.date === latestDate || x.date === prevDate).slice(-4);
        }
        
        let pairs = new Set();
        let subDigits = new Set();
        
        const getSubs = (str) => {
            let res = [];
            for (let i = 0; i < str.length - 1; i++) {
                res.push(str.slice(i, i+2));
                res.push(str.slice(i, i+2).split('').reverse().join(''));
            }
            if (str.length >= 2) {
                res.push(str[0] + str[str.length-1]);
                res.push(str[str.length-1] + str[0]);
            }
            return res;
        };

        for (let i = 0; i < todaysDraws.length - 1; i++) {
            let t1 = todaysDraws[i].tail;
            let t2 = todaysDraws[i+1].tail;
            
            let v1 = parseInt(t1);
            let r1 = parseInt(t1.split('').reverse().join(''));
            let r2 = parseInt(t2.split('').reverse().join(''));
            
            let m1 = String(v1 * r2);
            let m2 = String(r1 * r2);
            
            getSubs(m1).forEach(p => pairs.add(p));
            getSubs(m2).forEach(p => pairs.add(p));
            
            let s = String(Math.abs(parseInt(t1) - parseInt(t2))).padStart(3, '0');
            s.split('').forEach(d => subDigits.add(d));
        }
        
        return { pairs: Array.from(pairs).sort(), subDigits: Array.from(subDigits).sort() };
    }
"""

# Inject function into script if not exists
if 'function getCrossDayPools' not in content:
    content = content.replace('function findTopCombinations', js_logic + '\n    function findTopCombinations')


# Update the Active Baseline Box HTML template
target_active = r"""<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Column-wise Probability Matrix
                      </div>.*?</div>`.*?\}\)\(\)\}
                    </div>"""

new_active = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1 mb-1 border-b border-pink-200 pb-1">
                        \U0001f52e Cross-Day Pools (Multiplication & Subtraction)
                      </div>
                      ${(() => {
                          try {
                              const pools = getCrossDayPools(drawHistoryRecords);
                              if (pools) {
                                  return `
                                    <div class="text-left w-full px-2">
                                        <div class="text-[11px] text-pink-900 mb-1">
                                            <strong class="text-rose-700">Sub. Digits (Hot Singles):</strong> 
                                            <span class="font-mono text-sm bg-pink-100 px-1 rounded">${pools.subDigits.join(', ')}</span>
                                        </div>
                                        <div class="text-[10px] text-pink-900 leading-tight">
                                            <strong class="text-rose-700 block mb-0.5">M1/M2 Pairs Pool (AB, BC, AC candidates):</strong> 
                                            <div class="flex flex-wrap gap-x-1 gap-y-0.5 max-h-[60px] overflow-y-auto">
                                                ${pools.pairs.map(p => `<span class="bg-white border border-pink-100 rounded px-1">${p}</span>`).join('')}
                                            </div>
                                        </div>
                                    </div>
                                  `;
                              }
                          } catch(e) { console.error(e); }
                          return `<div class="text-[9px] text-pink-900">Calculating...</div>`;
                      })()}
                    </div>"""

content = re.sub(target_active, lambda m: new_active, content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

