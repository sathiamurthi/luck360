import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """<div class="text-[10px] font-black text-amber-900 uppercase"> \U0001f525 Derived AB Anchor Pair \U0001f525 </div>
                    <div class="text-[11px] text-amber-800 font-medium mt-0.5">
                      Formed by combining the <strong>last digit of H15</strong> and <strong>last digit of H14</strong>
                    </div>
                    <div class="text-2xl font-black text-rose-600 font-mono mt-1 tracking-widest">
                      [${activeResult.h15_val[2]}${activeResult.h14_val[2]}]
                    </div>"""

injection = """
<div class="text-[10px] font-black text-amber-900 uppercase"> \U0001f525 Derived AB Anchor Pair \U0001f525 </div>
                    <div class="text-[11px] text-amber-800 font-medium mt-0.5 flex flex-col gap-1 items-center justify-center">
                      <div>Anchor (H15.last + H14.last): <strong class="text-rose-600 font-mono text-sm">[${activeResult.h15_val[2]}${activeResult.h14_val[2]}]</strong></div>
                      
                      <div class="w-full h-px bg-amber-200 my-1"></div>
                      
                      <div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Master Formula Pair
                      </div>
                      ${(() => {
                          try {
                              const r = findDynamicMasterRules(drawHistoryRecords);
                              if (r && r.a && r.b) {
                                  const r1 = r.evalRule(r.a[0], activeResult);
                                  const r2 = r.evalRule(r.b[0], activeResult);
                                  return `<div class="text-[9px] text-pink-900 leading-tight mb-1">R1: ${r.a[0]} &nbsp;|&nbsp; R2: ${r.b[0]}</div>
                                          <div class="text-xl font-black text-pink-600 font-mono tracking-widest">
                                            [${r1}${r2}] / [${r2}${r1}]
                                          </div>`;
                              }
                          } catch(e) {}
                          return `<div class="text-[9px] text-pink-900">Calculating...</div>`;
                      })()}
                    </div>
"""

# wait, I need to match the emoji carefully
content = re.sub(r'<div class="text-\[10px\] font-black text-amber-900 uppercase">.*?\[\$\{activeResult\.h15_val\[2\]\}\$\{activeResult\.h14_val\[2\]\}\].*?</div>', lambda m: injection.strip(), content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
