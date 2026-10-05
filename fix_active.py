import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Top 3 ABC Scenarios (Next Draw)
                      </div>
                      ${(() => {
                          try {
                              const r = findDynamicMasterRules();
                              if (r) {
                                  let s = '';
                                  for (let i = 0; i < 3; i++) {
                                      const a = r.evalRule(r.a_rules[i].fn, activeResult);
                                      const b = r.evalRule(r.b_rules[i].fn, activeResult);
                                      const c = r.evalRule(r.c_rules[i].fn, activeResult);
                                      s += `<div class="text-[11px] text-pink-900 font-mono font-bold">Scenario ${i+1}: <span class="text-rose-600 text-sm tracking-widest ml-1">[${a}${b}${c}]</span></div>`;
                                  }
                                  return s;
                              }
                          } catch(e) { console.error(e); }
                          return `<div class="text-[9px] text-pink-900">Calculating...</div>`;
                      })()}
                    </div>"""

new_active = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Column-wise Probability Matrix
                      </div>
                      ${(() => {
                          try {
                              const r = findDynamicMasterRules();
                              if (r) {
                                  let a_vals = [], b_vals = [], c_vals = [];
                                  for (let i = 0; i < 3; i++) {
                                      a_vals.push(r.evalRule(r.a_rules[i].fn, activeResult));
                                      b_vals.push(r.evalRule(r.b_rules[i].fn, activeResult));
                                      c_vals.push(r.evalRule(r.c_rules[i].fn, activeResult));
                                  }
                                  
                                  const getProbs = (vals, weights) => {
                                      let counts = {}; let total = 0;
                                      for (let i=0; i<vals.length; i++) {
                                          counts[vals[i]] = (counts[vals[i]] || 0) + weights[i];
                                          total += weights[i];
                                      }
                                      return Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(e => `<strong class="text-rose-700 font-mono text-sm">${e[0]}</strong> <span class="text-[9px] text-slate-500">(${Math.round((e[1]/total)*100)}%)</span>`).join(' &nbsp; ');
                                  };
                                  
                                  const a_probs = getProbs(a_vals, [4, 4, 3]);
                                  const b_probs = getProbs(b_vals, [3, 3, 3]);
                                  const c_probs = getProbs(c_vals, [2, 2, 2]);
                                  
                                  return `
                                    <div class="text-[11px] text-pink-900 font-medium w-full text-left pl-2">
                                        <div class="mb-0.5">\ud83c\udd70\ufe0f Col A: ${a_probs}</div>
                                        <div class="mb-0.5">\ud83c\udd71\ufe0f Col B: ${b_probs}</div>
                                        <div>\u00a9\ufe0f Col C: ${c_probs}</div>
                                    </div>
                                  `;
                              }
                          } catch(e) { console.error(e); }
                          return `<div class="text-[9px] text-pink-900">Calculating...</div>`;
                      })()}
                    </div>"""

# we need to be careful with exact match because of whitespace
content = re.sub(r'<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">.*?Top 3 ABC Scenarios \(Next Draw\).*?</div>`.*?\)\(\)\}\n                    </div>', lambda m: new_active, content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
