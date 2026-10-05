import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
import re

new_js = r"""<div class="flex-1 p-2 bg-pink-50 border border-pink-200 rounded text-center shadow-sm">
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
                                  let v_curr = parseInt(curr);
                                  let r_curr = parseInt(curr.split('').reverse().join(''));
                                  let r_prev = parseInt(prev.split('').reverse().join(''));
                                  
                                  let m_dir = String(v_prev * v_curr);
                                  let m_r1 = String(r_prev * v_curr);
                                  let m_r2 = String(v_prev * r_curr);
                                  let m_r3 = String(r_prev * r_curr);
                                  let sub = String(Math.abs(v_prev - v_curr)).padStart(3, '0');
                                  
                                  const tail_r2 = m_r2.slice(-3).padStart(3, '0');
                                  const tail_r3 = m_r3.slice(-3).padStart(3, '0');

                                  const applyH15_17 = (tailStr) => {
                                      const t = tailStr.padStart(3, '0');
                                      const d1 = parseInt(t[0]), d2 = parseInt(t[1]), d3 = parseInt(t[2]);
                                      const h15 = `${(d2+1)%10}${(d3-d1+10)%10}${d1}`;
                                      const h17 = `${(d1+d2)%10}${(d1-d2+10)%10}${d3}`;
                                      return { h15, h17 };
                                  };

                                  const formatAB = (t) => `AB: ${t.substring(0,2)} | BC: ${t.substring(1,3)} | AC: ${t[0]+t[2]}`;

                                  const pats_r2 = applyH15_17(tail_r2);
                                  const pats_r3 = applyH15_17(tail_r3);
                                  
                                  mathHtml = '<div class="bg-pink-50 border border-pink-100 rounded p-1.5 mb-2 text-[9px] font-mono text-pink-900 text-left space-y-1">' +
                                        '<div><span class="font-bold text-rose-700">Direct:</span> ' + v_prev + '\u00d7' + v_curr + ' = ' + m_dir + ' \u2192 <strong class="text-rose-900">' + m_dir.slice(-3) + '</strong></div>' +
                                        '<div><span class="font-bold text-rose-700">Rev Prev \u00d7 Curr:</span> ' + r_prev + '\u00d7' + v_curr + ' = ' + m_r1 + ' \u2192 <strong class="text-rose-900">' + m_r1.slice(-3) + '</strong></div>' +
                                        '<div class="pt-1 border-t border-pink-200"><span class="font-bold text-rose-700">Prev \u00d7 Rev Curr:</span> ' + v_prev + '\u00d7' + r_curr + ' = ' + m_r2 + ' \u2192 <strong class="text-rose-900">' + tail_r2 + '</strong></div>' +
                                        '<div class="pl-2 text-[8px] text-pink-700">H15: ' + pats_r2.h15 + ' (' + formatAB(pats_r2.h15) + ') <br> H17: ' + pats_r2.h17 + ' (' + formatAB(pats_r2.h17) + ')</div>' +
                                        '<div class="pt-1"><span class="font-bold text-rose-700">Rev Prev \u00d7 Rev Curr:</span> ' + r_prev + '\u00d7' + r_curr + ' = ' + m_r3 + ' \u2192 <strong class="text-rose-900">' + tail_r3 + '</strong></div>' +
                                        '<div class="pl-2 text-[8px] text-pink-700">H15: ' + pats_r3.h15 + ' (' + formatAB(pats_r3.h15) + ') <br> H17: ' + pats_r3.h17 + ' (' + formatAB(pats_r3.h17) + ')</div>' +
                                        '<div class="pt-1 border-t border-pink-200 mt-1"><span class="font-bold text-rose-700">Abs Subtraction:</span> |' + prev + ' - ' + curr + '| = <strong class="text-rose-900">' + sub + '</strong> <br><span class="pl-2 text-[8px] text-pink-700">' + formatAB(sub) + '</span></div>' +
                                    '</div>';
                              }
"""

start_str = '<div class="flex-1 p-2 bg-pink-50 border border-pink-200 rounded text-center shadow-sm">'
idx = content.find(start_str)
end_str = "return mathHtml + targetHtml;"
idx_end = content.find(end_str, idx)

if idx != -1 and idx_end != -1:
    div_end = content.find('}', idx_end) # find the end of the if (targets) block
    content = content[:idx] + new_js + content[idx_end:]
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find blocks")
