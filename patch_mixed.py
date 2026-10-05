import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target1 = r"""              const get3DGuesses = \(pats\) => \{
                  if \(!pats \|\| !pats\.h14_val \|\| !pats\.h18_val\) return \[\];
                  const h14 = pats\.h14_val;
                  const h18 = pats\.h18_val;
                  if\(h14==='---' \|\| h18==='---'\) return \[\];
                  const g1 = h14\.split\(''\)\.reverse\(\)\.join\(''\);
                  const g2 = h18\[0\] \+ h18\[2\] \+ h18\[1\];
                  return \[\.\.\.new Set\(\[g1, g2\]\)\];
              \};"""

replacement1 = """              const get3DGuesses = (pats) => {
                  if (!pats || !pats.h14_val || !pats.h18_val) return [];
                  const h14 = pats.h14_val;
                  const h18 = pats.h18_val;
                  if(h14==='---' || h18==='---') return [];
                  const g1 = h14.split('').reverse().join('');
                  const g2 = h18[0] + h18[2] + h18[1];
                  return [...new Set([g1, g2])];
              };
              
              const getMixedCrossPairs = (pats15, pats17) => {
                  if (!pats15 || !pats17 || !pats15.h15_val || !pats17.h17_val) return [];
                  const h15 = pats15.h15_val;
                  const h17 = pats17.h17_val;
                  if(h15==='---' || h17==='---') return [];
                  return [...new Set([
                      h15[2] + h17[2],
                      h15[2] + h17[0],
                      h15[0] + h17[2],
                      h15[0] + h17[0],
                      h15[1] + h17[0],
                      h15[1] + h17[2]
                  ])];
              };"""

target2 = r"""                          <div class="flex justify-between text-\[9px\] font-mono leading-tight pt-0\.5">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0\.5 uppercase text-\[7\.5px\]">Head Base</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: \[\$\{getCrossPairs\(bHeadPats\)\.join\(','\)\}\]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0\.5">3D: \[\$\{get3DGuesses\(bHeadPats\)\.join\(','\)\}\]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0\.5 uppercase text-\[7\.5px\]">Head Target</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: \[\$\{getCrossPairs\(cHeadPats\)\.join\(','\)\}\]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0\.5">3D: \[\$\{get3DGuesses\(cHeadPats\)\.join\(','\)\}\]</span>
                              </div>
                          </div>
                      </div>"""

replacement2 = """                          <div class="flex justify-between text-[9px] font-mono leading-tight pt-0.5 border-b border-slate-200 pb-1.5">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Head Base</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(bHeadPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(bHeadPats).join(',')}]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Head Target</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(cHeadPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(cHeadPats).join(',')}]</span>
                              </div>
                          </div>
                          
                          <div class="flex justify-between text-[9px] font-mono leading-tight pt-1">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Mixed Base (H15-H &times; T-H17)</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getMixedCrossPairs(bHeadPats, bPats).join(',')}]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Mixed Target (H15-H &times; T-H17)</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getMixedCrossPairs(cHeadPats, cPats).join(',')}]</span>
                              </div>
                          </div>
                      </div>"""

if re.search(target1, content):
    content = re.sub(target1, replacement1, content)
    print("Patched target1!")
else:
    print("Target1 not found.")

if re.search(target2, content):
    content = re.sub(target2, replacement2, content)
    print("Patched target2!")
else:
    print("Target2 not found.")

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
