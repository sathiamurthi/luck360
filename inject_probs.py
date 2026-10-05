import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Active Baseline panel injection
target_active = r"""<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Top 3 ABC Scenarios \(Next Draw\)
                      </div>
                      \$\{\(\(\) => \{
                          try \{
                              const r = findDynamicMasterRules\(\);.*?\}\)\(\)\}
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
content = re.sub(target_active, lambda m: new_active, content, flags=re.DOTALL)


# 2. Update the History Table injection
target_history = r"""try \{\s*const r = typeof findDynamicMasterRules !== 'undefined'.*?catch\(e\) \{\s*console\.error\(e\);\s*\}"""

new_history = r"""
          try {
              const r = typeof findDynamicMasterRules !== 'undefined' ? findDynamicMasterRules() : null;
              if (r && fwd.H15_ShiftDiff) {
                  const mockPatterns = {
                      h15_val: String(fwd.H15_ShiftDiff),
                      h14_val: String(fwd.H14_PrefixDiff_615 || '000'),
                      h7_val:  String(fwd.H7_DiffDiffSum || '000'),
                      h16_val: String(fwd.H16_TwinEchoStep || '000'),
                      h17_val: String(fwd.H17_SumDiffKeep || '000')
                  };
                  let a_vals = [], b_vals = [], c_vals = [];
                  for (let i=0; i<3; i++) {
                      a_vals.push(r.evalRule(r.a_rules[i].fn, mockPatterns));
                      b_vals.push(r.evalRule(r.b_rules[i].fn, mockPatterns));
                      c_vals.push(r.evalRule(r.c_rules[i].fn, mockPatterns));
                  }
                  
                  const getProbs = (vals, weights) => {
                      let counts = {}; let total = 0;
                      for (let i=0; i<vals.length; i++) {
                          counts[vals[i]] = (counts[vals[i]] || 0) + weights[i];
                          total += weights[i];
                      }
                      return Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(e => `<strong>${e[0]}</strong><span style="font-size:8px">(${Math.round((e[1]/total)*100)}%)</span>`).join(' ');
                  };
                  
                  const a_probs = getProbs(a_vals, [4, 4, 3]);
                  const b_probs = getProbs(b_vals, [3, 3, 3]);
                  const c_probs = getProbs(c_vals, [2, 2, 2]);
                  
                  fwdCodes += `<div class="mt-1.5 p-1 bg-pink-50 rounded border border-pink-100 text-[10px] text-pink-900 leading-tight">
                    <div class="font-bold text-pink-700 mb-0.5">\U0001f52e Dynamic ABC Probability Matrix</div>
                    A: ${a_probs} <br> B: ${b_probs} <br> C: ${c_probs}
                  </div>`;
              }
          } catch(e) {
              console.error(e);
          }
"""
content = re.sub(target_history, lambda m: new_history.strip(), content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
