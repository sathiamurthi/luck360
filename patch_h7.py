import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""              let bHeadPats = \{ h17_val: '---', h15_val: '---', h14_val: '---' \};
              try \{ bHeadPats = calculateSingleDrawPatterns\(bHead\); \} catch\(e\)\{\}
              
              let cardStory = '';
              if \(cDraw\.ticket === 'PENDING'\) \{
                  cardStory = `
                      <div class="font-bold text-slate-800 text-\[10\.5px\] pb-1">
                          Awaiting <span class="text-indigo-900">\$\{cDraw\.time\}</span> Result for Confluence
                      </div>
                      <div class="bg-slate-50 border border-slate-200 rounded p-1\.5 space-y-1">
                          <div class="text-\[9px\] font-black text-slate-500 uppercase tracking-widest">Base Targets \(From Prev \$\{bTail\} &amp; \$\{bHead\}\)</div>
                          <div class="flex justify-between items-center border-b border-slate-200 pb-1 text-\[9\.5px\]">
                              <span class="font-bold text-amber-800">Tail H17: <span class="font-black text-amber-950">\$\{bPats\.h17_val\}</span></span>
                              <span class="font-bold text-amber-800">H15: <span class="font-black text-amber-950">\$\{bPats\.h15_val\}</span></span>
                              <span class="font-bold text-amber-800">H14: <span class="font-black text-amber-950">\$\{bPats\.h14_val \|\| '---'\}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0\.5 text-\[9\.5px\]">
                              <span class="font-bold text-emerald-800">Head H17: <span class="font-black text-emerald-950">\$\{bHeadPats\.h17_val\}</span></span>
                              <span class="font-bold text-emerald-800">H15: <span class="font-black text-emerald-950">\$\{bHeadPats\.h15_val\}</span></span>
                              <span class="font-bold text-emerald-800">H14: <span class="font-black text-emerald-950">\$\{bHeadPats\.h14_val\}</span></span>
                          </div>
                      </div>
                  `;
              \} else \{
                  const cExt = extractHeadAndTail\(cDraw\.ticket\);
                  const cTail = cExt\.tail;
                  const cHead = cExt\.head;
                  let cPats = \{ h17_val: '---', h15_val: '---', h14_val: '---' \}, cHeadPats = \{ h17_val: '---', h15_val: '---', h14_val: '---' \}, cBlind = \{ b2: '---' \};
                  try \{ cPats = calculateSingleDrawPatterns\(cTail\); cHeadPats = calculateSingleDrawPatterns\(cHead\); cBlind = calcBlindPatterns\(cTail\); \} catch\(e\)\{\}
                  
                  cardStory = `
                      <div class="font-bold text-slate-800 text-\[10\.5px\] pb-1 border-b border-amber-200 mb-1">
                          Ticket: <span class="text-indigo-900">\$\{cDraw\.ticket\}</span> \(Head: \$\{cHead\}, Tail: \$\{cTail\}\)
                      </div>
                      
                      <div class="bg-slate-50 border border-slate-200 rounded p-1\.5 space-y-1">
                          <div class="text-\[9px\] font-black text-slate-500 uppercase tracking-widest">Base Influences \(From Prev \$\{bTail\} &amp; \$\{bHead\}\)</div>
                          <div class="flex justify-between items-center border-b border-slate-200 pb-1 text-\[9\.5px\]">
                              <span class="font-bold text-amber-800">Tail H17: <span class="font-black text-amber-950">\$\{bPats\.h17_val\}</span></span>
                              <span class="font-bold text-amber-800">H15: <span class="font-black text-amber-950">\$\{bPats\.h15_val\}</span></span>
                              <span class="font-bold text-amber-800">H14: <span class="font-black text-amber-950">\$\{bPats\.h14_val \|\| '---'\}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0\.5 text-\[9\.5px\]">
                              <span class="font-bold text-emerald-800">Head H17: <span class="font-black text-emerald-950">\$\{bHeadPats\.h17_val\}</span></span>
                              <span class="font-bold text-emerald-800">H15: <span class="font-black text-emerald-950">\$\{bHeadPats\.h15_val\}</span></span>
                              <span class="font-bold text-emerald-800">H14: <span class="font-black text-emerald-950">\$\{bHeadPats\.h14_val\}</span></span>
                          </div>
                      </div>
                      
                      <div class="bg-amber-50 border border-amber-200 rounded p-1\.5 space-y-1 mt-1\.5">
                          <div class="text-\[9px\] font-black text-amber-700 uppercase tracking-widest">Generated Targets \(From Curr \$\{cTail\} &amp; \$\{cHead\}\)</div>
                          <div class="flex justify-between items-center border-b border-amber-200 pb-1 text-\[9\.5px\]">
                              <span class="font-bold text-indigo-800">Tail H17: <span class="font-black text-indigo-950">\$\{cPats\.h17_val\}</span></span>
                              <span class="font-bold text-indigo-800">H15: <span class="font-black text-indigo-950">\$\{cPats\.h15_val\}</span></span>
                              <span class="font-bold text-indigo-800">H14: <span class="font-black text-indigo-950">\$\{cPats\.h14_val \|\| '---'\}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0\.5 text-\[9\.5px\]">
                              <span class="font-bold text-rose-800">Head H17: <span class="font-black text-rose-950">\$\{cHeadPats\.h17_val\}</span></span>
                              <span class="font-bold text-rose-800">H15: <span class="font-black text-rose-950">\$\{cHeadPats\.h15_val\}</span></span>
                              <span class="font-bold text-rose-800">H14: <span class="font-black text-rose-950">\$\{cHeadPats\.h14_val\}</span></span>
                          </div>
                      </div>
                      
                      <div class="bg-purple-50 border border-purple-200 rounded p-1\.5 mt-1\.5">
                          <div class="text-\[9px\] font-black text-purple-700 uppercase tracking-widest mb-1">Abs Subtraction \(\|Curr - Prev\|\)</div>
                          <div class="flex justify-between items-center text-\[9\.5px\]">
                              <span class="font-bold text-purple-900">Tail \u0394: <span class="font-black bg-purple-200 px-1 rounded">\$\{String\(Math\.abs\(parseInt\(cTail \|\| 0\) - parseInt\(bTail \|\| 0\)\)\)\.padStart\(3, '0'\)\}</span></span>
                              <span class="font-bold text-purple-900">Head \u0394: <span class="font-black bg-purple-200 px-1 rounded">\$\{String\(Math\.abs\(parseInt\(cHead \|\| 0\) - parseInt\(bHead \|\| 0\)\)\)\.padStart\(3, '0'\)\}</span></span>
                          </div>
                      </div>
                  `;
              \}"""

replacement = """              let bHeadPats = { h17_val: '---', h15_val: '---', h14_val: '---', h7_val: '---' };
              try { bHeadPats = calculateSingleDrawPatterns(bHead); } catch(e){}
              
              let cardStory = '';
              if (cDraw.ticket === 'PENDING') {
                  cardStory = `
                      <div class="font-bold text-slate-800 text-[10.5px] pb-1">
                          Awaiting <span class="text-indigo-900">${cDraw.time}</span> Result for Confluence
                      </div>
                      <div class="bg-slate-50 border border-slate-200 rounded p-1.5 space-y-1">
                          <div class="text-[9px] font-black text-slate-500 uppercase tracking-widest">Base Targets (From Prev ${bTail} &amp; ${bHead})</div>
                          <div class="flex justify-between items-center border-b border-slate-200 pb-1 text-[8.5px]">
                              <span class="font-bold text-amber-800">T-H17: <span class="font-black text-amber-950">${bPats.h17_val}</span></span>
                              <span class="font-bold text-amber-800">H15: <span class="font-black text-amber-950">${bPats.h15_val}</span></span>
                              <span class="font-bold text-amber-800">H14: <span class="font-black text-amber-950">${bPats.h14_val || '---'}</span></span>
                              <span class="font-bold text-amber-800">H7: <span class="font-black text-amber-950">${bPats.h7_val || '---'}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0.5 text-[8.5px]">
                              <span class="font-bold text-emerald-800">H-H17: <span class="font-black text-emerald-950">${bHeadPats.h17_val}</span></span>
                              <span class="font-bold text-emerald-800">H15: <span class="font-black text-emerald-950">${bHeadPats.h15_val}</span></span>
                              <span class="font-bold text-emerald-800">H14: <span class="font-black text-emerald-950">${bHeadPats.h14_val}</span></span>
                              <span class="font-bold text-emerald-800">H7: <span class="font-black text-emerald-950">${bHeadPats.h7_val || '---'}</span></span>
                          </div>
                      </div>
                  `;
              } else {
                  const cExt = extractHeadAndTail(cDraw.ticket);
                  const cTail = cExt.tail;
                  const cHead = cExt.head;
                  let cPats = { h17_val: '---', h15_val: '---', h14_val: '---', h7_val: '---' }, cHeadPats = { h17_val: '---', h15_val: '---', h14_val: '---', h7_val: '---' }, cBlind = { b2: '---' };
                  try { cPats = calculateSingleDrawPatterns(cTail); cHeadPats = calculateSingleDrawPatterns(cHead); cBlind = calcBlindPatterns(cTail); } catch(e){}
                  
                  cardStory = `
                      <div class="font-bold text-slate-800 text-[10.5px] pb-1 border-b border-amber-200 mb-1">
                          Ticket: <span class="text-indigo-900">${cDraw.ticket}</span> (Head: ${cHead}, Tail: ${cTail})
                      </div>
                      
                      <div class="bg-slate-50 border border-slate-200 rounded p-1.5 space-y-1">
                          <div class="text-[9px] font-black text-slate-500 uppercase tracking-widest">Base Influences (From Prev ${bTail} &amp; ${bHead})</div>
                          <div class="flex justify-between items-center border-b border-slate-200 pb-1 text-[8.5px]">
                              <span class="font-bold text-amber-800">T-H17: <span class="font-black text-amber-950">${bPats.h17_val}</span></span>
                              <span class="font-bold text-amber-800">H15: <span class="font-black text-amber-950">${bPats.h15_val}</span></span>
                              <span class="font-bold text-amber-800">H14: <span class="font-black text-amber-950">${bPats.h14_val || '---'}</span></span>
                              <span class="font-bold text-amber-800">H7: <span class="font-black text-amber-950">${bPats.h7_val || '---'}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0.5 text-[8.5px]">
                              <span class="font-bold text-emerald-800">H-H17: <span class="font-black text-emerald-950">${bHeadPats.h17_val}</span></span>
                              <span class="font-bold text-emerald-800">H15: <span class="font-black text-emerald-950">${bHeadPats.h15_val}</span></span>
                              <span class="font-bold text-emerald-800">H14: <span class="font-black text-emerald-950">${bHeadPats.h14_val}</span></span>
                              <span class="font-bold text-emerald-800">H7: <span class="font-black text-emerald-950">${bHeadPats.h7_val || '---'}</span></span>
                          </div>
                      </div>
                      
                      <div class="bg-amber-50 border border-amber-200 rounded p-1.5 space-y-1 mt-1.5">
                          <div class="text-[9px] font-black text-amber-700 uppercase tracking-widest">Generated Targets (From Curr ${cTail} &amp; ${cHead})</div>
                          <div class="flex justify-between items-center border-b border-amber-200 pb-1 text-[8.5px]">
                              <span class="font-bold text-indigo-800">T-H17: <span class="font-black text-indigo-950">${cPats.h17_val}</span></span>
                              <span class="font-bold text-indigo-800">H15: <span class="font-black text-indigo-950">${cPats.h15_val}</span></span>
                              <span class="font-bold text-indigo-800">H14: <span class="font-black text-indigo-950">${cPats.h14_val || '---'}</span></span>
                              <span class="font-bold text-indigo-800">H7: <span class="font-black text-indigo-950">${cPats.h7_val || '---'}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0.5 text-[8.5px]">
                              <span class="font-bold text-rose-800">H-H17: <span class="font-black text-rose-950">${cHeadPats.h17_val}</span></span>
                              <span class="font-bold text-rose-800">H15: <span class="font-black text-rose-950">${cHeadPats.h15_val}</span></span>
                              <span class="font-bold text-rose-800">H14: <span class="font-black text-rose-950">${cHeadPats.h14_val}</span></span>
                              <span class="font-bold text-rose-800">H7: <span class="font-black text-rose-950">${cHeadPats.h7_val || '---'}</span></span>
                          </div>
                      </div>
                      
                      <div class="bg-purple-50 border border-purple-200 rounded p-1.5 mt-1.5">
                          <div class="text-[9px] font-black text-purple-700 uppercase tracking-widest mb-1">Abs Subtraction (|Curr - Prev|)</div>
                          <div class="flex justify-between items-center text-[9.5px]">
                              <span class="font-bold text-purple-900">Tail \u0394: <span class="font-black bg-purple-200 px-1 rounded">${String(Math.abs(parseInt(cTail || 0) - parseInt(bTail || 0))).padStart(3, '0')}</span></span>
                              <span class="font-bold text-purple-900">Head \u0394: <span class="font-black bg-purple-200 px-1 rounded">${String(Math.abs(parseInt(cHead || 0) - parseInt(bHead || 0))).padStart(3, '0')}</span></span>
                          </div>
                      </div>
                  `;
              }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched H7 successfully!")
else:
    print("Target block not found.")
