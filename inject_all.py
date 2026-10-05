import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update findDynamicMasterRules
new_find_rules = r"""
    function findDynamicMasterRules() {
        return {
            a_rules: [
                { name: '(H15.mid + H16.last)', fn: d => (d['H15.mid'] + d['H16.last']) % 10 },
                { name: '(H15.mid + H17.last + 1)', fn: d => (d['H15.mid'] + d['H17.last'] + 1) % 10 },
                { name: '|H14.last - H17.mid| - 1', fn: d => { let v = Math.abs(d['H14.last'] - d['H17.mid']) - 1; return v < 0 ? v + 10 : v; } }
            ],
            b_rules: [
                { name: '(H7.first + H17.last)', fn: d => (d['H7.first'] + d['H17.last']) % 10 },
                { name: '(H15.first + H16.last - 1)', fn: d => (d['H15.first'] + d['H16.last'] - 1 + 10) % 10 },
                { name: '(H16.mid + H16.last - 1)', fn: d => (d['H16.mid'] + d['H16.last'] - 1 + 10) % 10 }
            ],
            c_rules: [
                { name: '|H15.first - H15.mid|', fn: d => Math.abs(d['H15.first'] - d['H15.mid']) },
                { name: '(H16.first + H16.last - 1)', fn: d => (d['H16.first'] + d['H16.last'] - 1 + 10) % 10 },
                { name: '|H15.mid - H15.last| + 1', fn: d => (Math.abs(d['H15.mid'] - d['H15.last']) + 1) % 10 }
            ],
            evalRule: function(fn, patterns) {
                const d = {
                    'H15.first': parseInt(patterns.h15_val?.[0]||'0'), 'H15.mid': parseInt(patterns.h15_val?.[1]||'0'), 'H15.last': parseInt(patterns.h15_val?.[2]||'0'),
                    'H14.first': parseInt(patterns.h14_val?.[0]||'0'), 'H14.mid': parseInt(patterns.h14_val?.[1]||'0'), 'H14.last': parseInt(patterns.h14_val?.[2]||'0'),
                    'H7.first':  parseInt(patterns.h7_val?.[0]||'0'),  'H7.mid':  parseInt(patterns.h7_val?.[1]||'0'),  'H7.last':  parseInt(patterns.h7_val?.[2]||'0'),
                    'H16.first': parseInt(patterns.h16_val?.[0]||'0'), 'H16.mid': parseInt(patterns.h16_val?.[1]||'0'), 'H16.last': parseInt(patterns.h16_val?.[2]||'0'),
                    'H17.first': parseInt(patterns.h17_val?.[0]||'0'), 'H17.mid': parseInt(patterns.h17_val?.[1]||'0'), 'H17.last': parseInt(patterns.h17_val?.[2]||'0'),
                };
                return fn(d);
            }
        };
    }
"""

content = re.sub(r'function findDynamicMasterRules\(.*?\) \{.*?\n        \};\n    \}', lambda m: new_find_rules.strip(), content, flags=re.DOTALL)


# 2. Update the Active Baseline panel injection
target_active = r"""<div class="text-\[10px\] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
                        \U0001f52e Master Formula Pair
                      </div>.*?</div>`.*?\}\)\(\)\}
                    </div>"""

new_active = r"""<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">
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
content = re.sub(target_active, lambda m: new_active, content, flags=re.DOTALL)


# 3. Update the History Table injection
target_history = r"try \{\s*const r = typeof findDynamicMasterRules.*?catch\(e\) \{\s*console\.error\(e\);\s*\}"

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
                  let scen = [];
                  for (let i=0; i<3; i++) {
                      let a = r.evalRule(r.a_rules[i].fn, mockPatterns);
                      let b = r.evalRule(r.b_rules[i].fn, mockPatterns);
                      let c = r.evalRule(r.c_rules[i].fn, mockPatterns);
                      scen.push(`[${a}${b}${c}]`);
                  }
                  fwdCodes += `<br><span class="text-[10px] text-pink-700 font-bold bg-pink-50 px-1 py-0.5 rounded mt-1 inline-block">\U0001f52e Top 3 ABC Scenarios: ${scen.join('  ')}</span>`;
              }
          } catch(e) {
              console.error(e);
          }
"""
content = re.sub(target_history, lambda m: new_history.strip(), content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
