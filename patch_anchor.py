import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                      <div class="bg-purple-50 border border-purple-200 rounded p-1\.5 mt-1\.5">
                          <div class="text-\[9px\] font-black text-purple-700 uppercase tracking-widest mb-1">Abs Subtraction \(\|Curr - Prev\|\)</div>
                          <div class="flex justify-between items-center text-\[9\.5px\]">
                              <span class="font-bold text-purple-900">Tail \u0394: <span class="font-black bg-purple-200 px-1 rounded">\$\{String\(Math\.abs\(parseInt\(cTail \|\| 0\) - parseInt\(bTail \|\| 0\)\)\)\.padStart\(3, '0'\)\}</span></span>
                              <span class="font-bold text-purple-900">Head \u0394: <span class="font-black bg-purple-200 px-1 rounded">\$\{String\(Math\.abs\(parseInt\(cHead \|\| 0\) - parseInt\(bHead \|\| 0\)\)\)\.padStart\(3, '0'\)\}</span></span>
                          </div>
                      </div>
                  `;
              \}"""

replacement = """                      <div class="bg-purple-50 border border-purple-200 rounded p-1.5 mt-1.5">
                          <div class="text-[9px] font-black text-purple-700 uppercase tracking-widest mb-1">Abs Subtraction (|Curr - Prev|)</div>
                          <div class="flex justify-between items-center text-[9.5px]">
                              <span class="font-bold text-purple-900">Tail \u0394: <span class="font-black bg-purple-200 px-1 rounded">${String(Math.abs(parseInt(cTail || 0) - parseInt(bTail || 0))).padStart(3, '0')}</span></span>
                              <span class="font-bold text-purple-900">Head \u0394: <span class="font-black bg-purple-200 px-1 rounded">${String(Math.abs(parseInt(cHead || 0) - parseInt(bHead || 0))).padStart(3, '0')}</span></span>
                          </div>
                      </div>
                      
                      <div class="flex gap-1 mt-1.5">
                          <div class="flex-1 bg-slate-800 rounded p-1 text-center">
                              <div class="text-[8px] font-bold text-slate-300 uppercase">Base Anchor</div>
                              <div class="text-[10px] font-mono text-emerald-400 font-black">
                                  H15+H14 = [${bPats.h15_val ? bPats.h15_val[2] : '-'}${bPats.h14_val ? bPats.h14_val[2] : '-'}]
                              </div>
                          </div>
                          <div class="flex-1 bg-slate-800 rounded p-1 text-center">
                              <div class="text-[8px] font-bold text-slate-300 uppercase">Curr Anchor</div>
                              <div class="text-[10px] font-mono text-amber-400 font-black">
                                  H15+H14 = [${cPats.h15_val ? cPats.h15_val[2] : '-'}${cPats.h14_val ? cPats.h14_val[2] : '-'}]
                              </div>
                          </div>
                      </div>
                  `;
              }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched Anchor Pair successfully!")
else:
    print("Target block not found.")
