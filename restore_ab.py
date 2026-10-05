import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
import re
new_active = r"""<div class="text-[10px] font-black text-amber-900 uppercase"> Derived AB Anchor Pair </div>
                    <div class="text-[11px] text-amber-800 font-medium mt-0.5">
                      Formed by combining the <strong>last digit of H15</strong> and <strong>last digit of H14</strong>
                    </div>
                    <div class="text-2xl font-black text-rose-600 font-mono mt-1 tracking-widest">
                      [${activeResult.h15_val[2]}${activeResult.h14_val[2]}]
                    </div>
                  </div>
                  <div class="flex-1 p-2 bg-pink-50 border border-pink-200 rounded text-center shadow-sm">
                      <div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1 mb-1 border-b border-pink-200 pb-1">
                        \u{1f3af} Cross-Day Generated Targets
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
                                  
                                  mathHtml = '<div class="bg-pink-50 border border-pink-100 rounded p-1 mb-2 text-[9px] font-mono text-pink-800 text-left">' +
                                        '<div><span class="font-bold text-rose-700">M1 (Prev \u00d7 RevCurr):</span> ' + v_prev + '\u00d7' + r_curr + ' = ' + m1 + ' ^ <strong class="text-rose-900 text-[10px]">' + m1.slice(-3) + '</strong></div>' +
                                        '<div><span class="font-bold text-rose-700">M2 (RevPrev \u00d7 RevCurr):</span> ' + r_prev + '\u00d7' + r_curr + ' = ' + m2 + ' ^ <strong class="text-rose-900 text-[10px]">' + m2.slice(-3) + '</strong></div>' +
                                        '<div class="mt-0.5"><span class="font-bold text-rose-700">Abs Subtraction:</span> |' + prev + ' - ' + curr + '| = <strong class="text-rose-900 text-[10px]">' + sub + '</strong></div>' +
                                    '</div>';
                              }
                              
                              const targets = typeof getCrossDayTargets !== 'undefined' ? getCrossDayTargets(drawHistoryRecords) : null;
                              if (targets && targets.length > 0) {
                                  let targetHtml = '<div class="text-left w-full px-2">';
                                  targets.forEach(t => {
                                      targetHtml += '<div class="mb-1 text-[11px] text-pink-900 border-b border-pink-50 pb-1 flex items-center">' +
                                                '<strong class="text-rose-700 text-xs bg-pink-100 px-1 rounded shadow-sm mr-2">\u{1f3af} [' + t.abc + ']</strong>' +
                                                '<span class="font-mono text-[10px] tracking-tight">' +
                                                    '<span class="text-slate-500">AB:</span><strong class="text-pink-800">' + t.ab + '</strong> | ' +
                                                    '<span class="text-slate-500">BC:</span><strong class="text-pink-800">' + t.bc + '</strong> | ' +
                                                    '<span class="text-slate-500">AC:</span><strong class="text-pink-800">' + t.ac + '</strong>' +
                                                '</span>' +
                                            '</div>';
                                  });
                                  targetHtml += '</div>';
                                  return mathHtml + targetHtml;
                              }
                          } catch(e) { console.error(e); }
                          return '<div class="text-[9px] text-pink-900">Calculating Targets...</div>';
                      })()}
"""

idx = content.find("Cross-Day Generated Targets")
if idx != -1:
    div_start = content.rfind('<div class="text-[10px]', 0, idx)
    end_str = "Calculating Targets...</div>';\n                      })()"
    idx_end = content.find(end_str, div_start)
    if idx_end != -1:
        div_end = idx_end + len(end_str)
        content = content[:div_start] + new_active + content[div_end:]
        with io.open('script1.js', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Restored Derived AB Anchor Pair successfully!")
    else:
        print("Failed to find end str")
else:
    print("Failed to find cross day")
