# -*- coding: utf-8 -*-
import io

new_js = r"""const bannerEl = document.getElementById('banner-hottest-recommendations');
      if (bannerEl) {
        let baseSlot = '';
        let activeVal = '';
        let a_h = '944';
        let a_t = '406';
        let nextSlotNameStr = '';
        
        if (is8PMComplete) {
            baseSlot = '8 PM'; activeVal = val4; nextSlotNameStr = 'Tomorrow 1:00 PM (Dear Day)';
        } else if (is6PMComplete) {
            baseSlot = '6 PM'; activeVal = val3; nextSlotNameStr = 'Tonight 8:00 PM (Dear Seagull)';
        } else if (is3pmReflected) {
            baseSlot = '3 PM'; activeVal = val2; nextSlotNameStr = 'Tonight 6:00 PM (Sikkim State Lottery)';
        } else if (is1pmReflected) {
            baseSlot = '1 PM'; activeVal = val1; nextSlotNameStr = 'Today 3:00 PM (Kerala State)';
        } else {
            baseSlot = '8 PM (Prev)'; activeVal = val4 || '50E 94406'; nextSlotNameStr = 'Today 1:00 PM (Dear Day)';
        }

        const headTailBase = extractHeadAndTail(activeVal);
        a_h = headTailBase.head;
        a_t = headTailBase.tail;
        
        const headResultBase = calculateSingleDrawPatterns(a_h);
        const tailResultBase = calculateSingleDrawPatterns(a_t);
        const blindHeadBase = calcBlindPatterns(a_h);
        const blindTailBase = calcBlindPatterns(a_t);

        const t1_tail = t1 || '053';
        const t1_res = calculateSingleDrawPatterns(t1_tail);
        const t1_blind = calcBlindPatterns(t1_tail);
        
        const t1_val = blindTailBase.b2;
        const t2_val = tailResultBase.h17_val;
        const t3_val = headResultBase.h9_val;
        const t4_val_target = t1_blind.b1;
        const t5_val = blindHeadBase.b4;
        const t6_val = t1_res.h17_val;
        const t7_val = tailResultBase.h16_val;
        const t8_val = headResultBase.h15_val;
        
        const pH8 = tailResultBase;
        
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
                return { h15: `${(d2+1)%10}${(d3-d1+10)%10}${d1}`, h17: `${(d1+d2)%10}${(d1-d2+10)%10}${d3}` };
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
        
        bannerEl.innerHTML = `
            <div class="space-y-3 w-full">
              <div class="flex flex-wrap items-center justify-between gap-2 border-b border-amber-300 pb-2">
                <div class="flex items-center gap-2 text-sm font-black text-amber-950 uppercase tracking-wider">
                  <span class="text-xl">\uD83D\uDD25</span> VERY HOTTEST RECOMMENDED CHOICE: <strong>${nextSlotNameStr}</strong>
                </div>
                <div class="flex flex-wrap items-center gap-1.5">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black bg-emerald-500 text-white shadow-xs">
                     H17 HIT PROVED
                  </span>
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black bg-teal-600 text-white shadow-xs">
                    BLIND T2 &amp; T4 ACTIVE
                  </span>
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black bg-purple-600 text-white shadow-xs">
                    ${t1_tail} 24H PATTERNS INTEGRATED
                  </span>
                  <span class="px-3 py-1 rounded-full text-[11px] font-mono font-black bg-amber-400 text-slate-900 border border-amber-500 shadow-sm animate-pulse">
                    FRONT PAIR ${t3_val.slice(0,2)} TRIPLE-LOCKED
                  </span>
                </div>
              </div>
              <p class="text-xs text-slate-800 font-medium font-sans leading-relaxed">
                <strong>Dual Confluence + Blind, 2 Additional Patterns &amp; ${t1_tail} 24H Cycle:</strong> Applied across ${baseSlot} winning ticket <strong>${activeVal}</strong> (Head <strong>${a_h}</strong>, Tail <strong>${a_t}</strong>) and previous Dear 1 PM result <strong>${t1_tail}</strong>. 
                Your discovered <strong>Star H17</strong> on Tail ${a_t} yields <strong>${t2_val} \u2605</strong>! 
                Head H8 + <strong>Tail Blind T2</strong> converge on <strong>${t1_val} \u2605</strong>, and <strong>\u2605 Star H9 on Head ${a_h}</strong> yields <strong>${t3_val} \u2605</strong>. 
                From 1 PM <strong>${t1_tail}</strong>, the 24-hour bypass leap delivers <strong>${t4_val_target} \u2605</strong>, while H17 on ${t1_tail} yields <strong>${t6_val} \u2605</strong>, locking Front-Twin <strong>${t6_val.slice(0,2)}</strong> alongside Head Blind T4 <strong>${t5_val} \u2605</strong> and H15 <strong>${t8_val} \u2605</strong>.
              </p>

              <div class="mt-4 p-3 bg-gradient-to-r from-slate-100 to-slate-200 border border-slate-300 rounded-lg shadow-inner">
                <div class="text-xs font-black text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-300 pb-1 flex items-center justify-between">
                  <span> ACTIVE BASELINE: <strong class="text-indigo-900">${a_t}</strong>  NEXT DIRECT TARGETS</span>
                  <span class="text-[10px] bg-slate-800 text-white px-2 py-0.5 rounded">H15, H14, H7, H17, H16</span>
                </div>
                
                <div class="mb-3 flex flex-col md:flex-row gap-2">
                  <div class="flex-1 p-2 bg-amber-50 border border-amber-200 rounded text-center shadow-sm">
                    <div class="text-[10px] font-black text-amber-900 uppercase"> Derived AB Anchor Pair </div>
                    <div class="text-[11px] text-amber-800 font-medium mt-0.5">
                      Formed by combining the <strong>last digit of H15</strong> and <strong>last digit of H14</strong>
                    </div>
                    <div class="text-2xl font-black text-rose-600 font-mono mt-1 tracking-widest">
                      [${tailResultBase.h15_val[2]}${tailResultBase.h14_val[2]}]
                    </div>
                  </div>
                  <div class="flex-1 p-2 bg-pink-50 border border-pink-200 rounded text-center shadow-sm">
                      <div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1 mb-1 border-b border-pink-200 pb-1">
                        \uD83C\uDFAF Cross-Day Generated Targets
                      </div>
                      ${mathHtml}
                  </div>
                </div>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div class="bg-white p-3 rounded-xl border border-amber-300 shadow-xs space-y-1">
                    <span class="text-[9px] uppercase font-black text-emerald-700 block">TOP TARGET #1 (TAIL BLIND T2)</span>
                    <div class="text-2xl font-black text-slate-900 tracking-wider">${t1_val} \u2605</div>
                    <div class="text-[10px] text-slate-600 font-sans">Derived: Tail ${a_t} (Blind Leap)</div>
                    <div class="text-[10px] font-mono text-emerald-800 font-bold">Pairs: AB [${t1_val.slice(0,2)}] | BC [${t1_val.slice(1,3)}]</div>
                  </div>
                  <div class="bg-white p-3 rounded-xl border border-amber-300 shadow-xs space-y-1">
                    <span class="text-[9px] uppercase font-black text-amber-700 block">TOP TARGET #2 (HEAD USER H9)</span>
                    <div class="text-2xl font-black text-slate-900 tracking-wider">${t3_val} \u2605</div>
                    <div class="text-[10px] text-slate-600 font-sans">Derived: Head ${a_h} (Sub-Add)</div>
                    <div class="text-[10px] font-mono text-emerald-800 font-bold">Pairs: AB [${t3_val.slice(0,2)}] | BC [${t3_val.slice(1,3)}]</div>
                  </div>
                  <div class="bg-white p-3 rounded-xl border border-amber-300 shadow-xs space-y-1">
                    <span class="text-[9px] uppercase font-black text-indigo-700 block">TOP TARGET #3 (SHIFT-DIFF H15)</span>
                    <div class="text-2xl font-black text-slate-900 tracking-wider">${pH8.h15_val} \u2605</div>
                    <div class="text-[10px] text-slate-600 font-sans">Derived: Head ${a_h} (Shift-Difference)</div>
                    <div class="text-[10px] font-mono text-emerald-800 font-bold">Pairs: AB [${pH8.h15_val.slice(0,2)}] | BC [${pH8.h15_val.slice(1,3)}]</div>
                  </div>
                  <div class="bg-white p-3 rounded-xl border border-amber-300 shadow-xs space-y-1">
                    <span class="text-[9px] uppercase font-black text-purple-700 block">TOP TARGET #4 (HEAD USER H17)</span>
                    <div class="text-2xl font-black text-slate-900 tracking-wider">${pH8.h17_val} \u2605</div>
                    <div class="text-[10px] text-slate-600 font-sans">Derived: Head ${a_h} (Sum-Diff-Keep)</div>
                    <div class="text-[10px] font-mono text-emerald-800 font-bold">Pairs: AB [${pH8.h17_val.slice(0,2)}] | BC [${pH8.h17_val.slice(1,3)}]</div>
                  </div>
                </div>
                
                <div class="mt-3 bg-amber-100/70 p-2.5 rounded-xl border border-amber-300 text-xs font-mono flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <strong class="text-amber-950 font-bold">Top Consensus AB Pairs:</strong>
                    <span class="font-black text-indigo-950 ml-1">44 \u2605 (Double-Locked), 55, 35, 41, 40, 94</span>
                  </div>
                  <div>
                    <strong class="text-amber-950 font-bold">Proven Precedents Today:</strong>
                    <span class="text-emerald-900 font-bold ml-1">226\u2192406 (100% Hit H17) | 615\u2192626 (100% Hit H16) | 053\u2192615 (100% Hit H14)</span>
                  </div>
                </div>
              </div>
            </div>
        `;
      }
"""

content = io.open('script1.js', 'r', encoding='utf-8').read()
start_marker = "const bannerEl = document.getElementById('banner-hottest-recommendations');"
idx_start = content.find(start_marker)
end_marker = "// Populate TOP 7 RULES"
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_content = content[:idx_start] + new_js + "    \n      " + content[idx_end:]
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated banner logic!")
else:
    print("Could not find markers.")
