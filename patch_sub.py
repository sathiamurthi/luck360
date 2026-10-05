import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                      <div class="bg-amber-50 border border-amber-200 rounded p-1\.5 space-y-1 mt-1\.5">
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
                  `;
              \}"""

replacement = """                      <div class="bg-amber-50 border border-amber-200 rounded p-1.5 space-y-1 mt-1.5">
                          <div class="text-[9px] font-black text-amber-700 uppercase tracking-widest">Generated Targets (From Curr ${cTail} &amp; ${cHead})</div>
                          <div class="flex justify-between items-center border-b border-amber-200 pb-1 text-[9.5px]">
                              <span class="font-bold text-indigo-800">Tail H17: <span class="font-black text-indigo-950">${cPats.h17_val}</span></span>
                              <span class="font-bold text-indigo-800">H15: <span class="font-black text-indigo-950">${cPats.h15_val}</span></span>
                              <span class="font-bold text-indigo-800">H14: <span class="font-black text-indigo-950">${cPats.h14_val || '---'}</span></span>
                          </div>
                          <div class="flex justify-between items-center pt-0.5 text-[9.5px]">
                              <span class="font-bold text-rose-800">Head H17: <span class="font-black text-rose-950">${cHeadPats.h17_val}</span></span>
                              <span class="font-bold text-rose-800">H15: <span class="font-black text-rose-950">${cHeadPats.h15_val}</span></span>
                              <span class="font-bold text-rose-800">H14: <span class="font-black text-rose-950">${cHeadPats.h14_val}</span></span>
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
    print("Patched subtraction successfully!")
else:
    print("Target block not found.")
