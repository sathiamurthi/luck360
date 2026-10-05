import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_logic = """
    function getCrossDayPools(history) {
        if (!history || history.length < 2) return null;
        let validDraws = history.filter(x => x.tail && x.tail.length === 3);
        if (validDraws.length < 2) return null;
        
        let latestDate = validDraws[validDraws.length - 1].date;
        let todaysDraws = validDraws.filter(x => x.date === latestDate);
        
        if (todaysDraws.length < 2) {
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

if 'function getCrossDayPools' not in content:
    content = content.replace('function findTopCombinations', js_logic + '\n    function findTopCombinations')


new_active = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1 mb-1 border-b border-pink-200 pb-1">
                        \U0001f52e Cross-Day Pools (M1/M2 & Subtraction)
                      </div>
                      ${(() => {
                          try {
                              const pools = getCrossDayPools(drawHistoryRecords);
                              if (pools) {
                                  return `
                                    <div class="text-left w-full px-2 mt-1">
                                        <div class="text-[11px] text-pink-900 mb-1.5 flex flex-col items-center">
                                            <strong class="text-rose-700 text-[9px] uppercase tracking-wider mb-0.5">\u2728 Subtraction Target Digits \u2728</strong> 
                                            <span class="font-mono text-sm bg-pink-100 text-pink-800 px-2 py-0.5 rounded shadow-inner tracking-widest font-bold">${pools.subDigits.join(', ')}</span>
                                        </div>
                                        <div class="text-[10px] text-pink-900 leading-tight border-t border-pink-100 pt-1.5">
                                            <strong class="text-rose-700 block mb-1 text-center">\ud83c\udfaf M1/M2 Pairs Pool (AB, BC, AC candidates):</strong> 
                                            <div class="flex flex-wrap gap-x-1 gap-y-1 max-h-[65px] overflow-y-auto justify-center px-1">
                                                ${pools.pairs.map(p => `<span class="bg-white border border-pink-200 text-pink-800 font-mono font-bold rounded px-1 shadow-sm">${p}</span>`).join('')}
                                            </div>
                                        </div>
                                    </div>
                                  `;
                              }
                          } catch(e) { console.error(e); }
                          return `<div class="text-[9px] text-pink-900">Calculating...</div>`;
                      })()}
                    </div>"""

content = re.sub(r'<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">.*?Column-wise Probability Matrix.*?</div>\s*\$\{\(\(\) => \{.*?\n                                  return `.*?</div>\n                                  `;\n                              \}\n                          \} catch\(e\) \{ console\.error\(e\); \}\n                          return `<div class="text-\[9px\] text-pink-900">Calculating...</div>`;\n                      \}\)\(\)\}\n                    </div>', lambda m: new_active, content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

