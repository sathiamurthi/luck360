import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

js_logic = """
    function getCrossDayTargets(history) {
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
        let subPool = [];
        
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
            let weight = i + 1; // More recent = higher weight
            for (let w = 0; w < weight; w++) {
                s.split('').forEach(d => subPool.push(d));
            }
        }
        
        let subCounts = {};
        subPool.forEach(d => subCounts[d] = (subCounts[d] || 0) + 1);
        
        let scores = [];
        for (let num = 0; num < 1000; num++) {
            let abc = String(num).padStart(3, '0');
            let ab = abc.slice(0, 2);
            let bc = abc.slice(1, 3);
            let ac = abc[0] + abc[2];
            
            let pair_score = 0;
            if (pairs.has(ab)) pair_score++;
            if (pairs.has(bc)) pair_score++;
            if (pairs.has(ac)) pair_score++;
            
            if (pair_score === 0) continue;
            
            let sub_score = 0;
            if (subCounts[abc[0]]) sub_score += subCounts[abc[0]] * 0.32;
            if (subCounts[abc[1]]) sub_score += subCounts[abc[1]] * 0.44;
            if (subCounts[abc[2]]) sub_score += subCounts[abc[2]] * 0.50;
            
            let total_score = (pair_score * 50) + sub_score;
            scores.push({abc, ab, bc, ac, score: total_score});
        }
        
        scores.sort((a, b) => b.score - a.score);
        return scores.slice(0, 5);
    }
"""

if 'function getCrossDayTargets' not in content:
    content = content.replace('function findDynamicMasterRules', js_logic + '\n    function findDynamicMasterRules')

# We need to replace the panel block in script1.js
# Searching for: Column-wise Probability Matrix
# wait, yesterday I injected the Probability Matrix into script1.js? Yes!
new_active = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1 mb-1 border-b border-pink-200 pb-1">
                        \ud83c\udfaf Cross-Day Generated Targets
                      </div>
                      ${(() => {
                          try {
                              let mathHtml = '';
                              const validDraws = drawHistoryRecords.filter(x => x.tail && x.tail.length === 3);
                              if (validDraws.length >= 2) {
                                  let curr = validDraws[validDraws.length - 1].tail;
                                  let prev = validDraws[validDraws.length - 2].tail;
                                  let v_prev = parseInt(prev);
                                  let r_curr = parseInt(curr.split('').reverse().join(''));
                                  let r_prev = parseInt(prev.split('').reverse().join(''));
                                  
                                  let m1 = String(v_prev * r_curr);
                                  let m2 = String(r_prev * r_curr);
                                  let sub = String(Math.abs(parseInt(prev) - parseInt(curr))).padStart(3, '0');
                                  
                                  mathHtml = `
                                    <div class="bg-pink-50 border border-pink-100 rounded p-1 mb-2 text-[9px] font-mono text-pink-800 text-left">
                                        <div><span class="font-bold text-rose-700">M1 (Prev \u00d7 RevCurr):</span> ${v_prev}\u00d7${r_curr} = ${m1} ^ ${m1.slice(-3)}</div>
                                        <div><span class="font-bold text-rose-700">M2 (RevPrev \u00d7 RevCurr):</span> ${r_prev}\u00d7${r_curr} = ${m2} ^ ${m2.slice(-3)}</div>
                                        <div class="mt-0.5"><span class="font-bold text-rose-700">Abs Subtraction:</span> |${prev} - ${curr}| = ${sub}</div>
                                    </div>
                                  `;
                              }
                              
                              const targets = typeof getCrossDayTargets !== 'undefined' ? getCrossDayTargets(drawHistoryRecords) : null;
                              if (targets && targets.length > 0) {
                                  return mathHtml + `
                                    <div class="text-left w-full px-2">
                                        ${targets.map((t, idx) => `
                                            <div class="mb-1 text-[11px] text-pink-900 border-b border-pink-50 pb-1 flex items-center">
                                                <strong class="text-rose-700 text-xs bg-pink-100 px-1 rounded shadow-sm mr-2">\ud83c\udfaf [${t.abc}]</strong> 
                                                <span class="font-mono text-[10px] tracking-tight">
                                                    <span class="text-slate-500">AB:</span><strong class="text-pink-800">${t.ab}</strong> | 
                                                    <span class="text-slate-500">BC:</span><strong class="text-pink-800">${t.bc}</strong> | 
                                                    <span class="text-slate-500">AC:</span><strong class="text-pink-800">${t.ac}</strong>
                                                </span>
                                            </div>
                                        `).join('')}
                                    </div>
                                  `;
                              }
                          } catch(e) { console.error(e); }
                          return `<div class="text-[9px] text-pink-900">Calculating Targets...</div>`;
                      })()}
                    </div>"""

# Let's find the exact string to replace in script1.js
# It should be the Column-wise probability matrix block.
target_active_old = r'<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">\s*\\U0001f52e Column-wise Probability Matrix\s*</div>.*?</div>`.*?\}\)\(\)\}\s*</div>'

content = re.sub(target_active_old, lambda m: new_active, content, flags=re.DOTALL)

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected into script1.js")

