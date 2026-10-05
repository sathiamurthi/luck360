import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                      <div class="bg-slate-100 border border-slate-300 rounded p-1\.5 mt-1\.5 shadow-inner">
                          <div class="text-\[8\.5px\] font-black text-slate-600 uppercase tracking-widest text-center border-b border-slate-200 pb-0\.5 mb-1">Cross-Pattern Synthesizer \(H15 &times; H17 &amp; H14/H18\)</div>
                          <div class="flex justify-between text-\[9px\] font-mono leading-tight">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0\.5 uppercase text-\[7\.5px\]">Base Math</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: \[\$\{getCrossPairs\(bPats\)\.join\(','\)\}\]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0\.5">3D: \[\$\{get3DGuesses\(bPats\)\.join\(','\)\}\]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0\.5 uppercase text-\[7\.5px\]">Target Math</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: \[\$\{getCrossPairs\(cPats\)\.join\(','\)\}\]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0\.5">3D: \[\$\{get3DGuesses\(cPats\)\.join\(','\)\}\]</span>
                              </div>
                          </div>
                      </div>"""

replacement = """                      <div class="bg-slate-100 border border-slate-300 rounded p-1.5 mt-1.5 shadow-inner space-y-1.5">
                          <div class="text-[8.5px] font-black text-slate-600 uppercase tracking-widest text-center border-b border-slate-200 pb-0.5 mb-1">Cross-Pattern Synthesizer (H15 &times; H17 &amp; H14/H18)</div>
                          
                          <div class="flex justify-between text-[9px] font-mono leading-tight border-b border-slate-200 pb-1.5">
                              <div class="flex flex-col">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Tail Base</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(bPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(bPats).join(',')}]</span>
                              </div>
                              <div class="flex flex-col text-right">
                                  <span class="text-slate-400 font-bold mb-0.5 uppercase text-[7.5px]">Tail Target</span>
                                  <span class="text-indigo-800 font-black tracking-tighter">AB: [${getCrossPairs(cPats).join(',')}]</span>
                                  <span class="text-rose-800 font-black tracking-tighter mt-0.5">3D: [${get3DGuesses(cPats).join(',')}]</span>
                              </div>
                          </div>
                          
                          <div class="flex justify-between text-[9px] font-mono leading-tight pt-0.5">
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
                      </div>"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched head logic successfully!")
else:
    print("Target block not found.")
