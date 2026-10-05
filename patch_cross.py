import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                          <div class="flex-1 bg-slate-800 rounded p-1 text-center">
                              <div class="text-\[8px\] font-bold text-slate-300 uppercase">Curr Anchor</div>
                              <div class="text-\[10px\] font-mono text-amber-400 font-black">
                                  H15\+H14 = \[\$\{cPats\.h15_val \? cPats\.h15_val\[2\] : '-'\}\$\{cPats\.h14_val \? cPats\.h14_val\[2\] : '-'\}\]
                              </div>
                          </div>
                      </div>
                  `;"""

replacement = """                          <div class="flex-1 bg-slate-800 rounded p-1 text-center">
                              <div class="text-[8px] font-bold text-slate-300 uppercase">Curr Anchor</div>
                              <div class="text-[10px] font-mono text-amber-400 font-black">
                                  H15+H14 = [${cPats.h15_val ? cPats.h15_val[2] : '-'}${cPats.h14_val ? cPats.h14_val[2] : '-'}]
                              </div>
                          </div>
                      </div>
                      
                      <div class="bg-slate-100 border border-slate-300 rounded p-1.5 mt-1.5 shadow-inner">
                          <div class="text-[8.5px] font-black text-slate-600 uppercase tracking-widest text-center border-b border-slate-200 pb-0.5 mb-1">Cross-Pattern Synthesizer (H15 &times; H17 &amp; H14/H18)</div>
                          <div class="flex justify-between text-[9px] font-mono leading-tight">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Base Math</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(bPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(bPats).join(',')}]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Target Math</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(cPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(cPats).join(',')}]</span>
                              </div>
                          </div>
                      </div>
                  `;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    # Also add the helper functions above the loop
    helper_code = """
              const getCrossPairs = (pats) => {
                  if (!pats || !pats.h15_val || !pats.h17_val) return [];
                  const h15 = pats.h15_val;
                  const h17 = pats.h17_val;
                  if(h15==='---' || h17==='---') return [];
                  return [...new Set([
                      h15[2] + h17[2],
                      h15[2] + h17[0],
                      h15[0] + h17[2],
                      h15[0] + h17[0]
                  ])];
              };
              
              const get3DGuesses = (pats) => {
                  if (!pats || !pats.h14_val || !pats.h18_val) return [];
                  const h14 = pats.h14_val;
                  const h18 = pats.h18_val;
                  if(h14==='---' || h18==='---') return [];
                  const g1 = h14.split('').reverse().join('');
                  const g2 = h18[0] + h18[2] + h18[1];
                  return [...new Set([g1, g2])];
              };
"""
    if "const getCrossPairs" not in content:
        # insert right before `let cardsHtml = '';`
        content = content.replace("let cardsHtml = '';", helper_code + "\nlet cardsHtml = '';")

    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched cross logic successfully!")
else:
    print("Target block not found.")
