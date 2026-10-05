import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = r"let fwdCodes = `H15: \$\{fwd\.H15_ShiftDiff \|\| '-'\} \| H14: \$\{fwd\.H14_PrefixDiff_615 \|\| '-'\} \| H7: \$\{fwd\.H7_DiffDiffSum \|\| '-'\}`;"

def replacer(m):
    return """
          let fwdCodes = `H15: ${fwd.H15_ShiftDiff || '-'} | H14: ${fwd.H14_PrefixDiff_615 || '-'} | H7: ${fwd.H7_DiffDiffSum || '-'}`;
          
          try {
              const r = typeof findDynamicMasterRules !== 'undefined' ? findDynamicMasterRules(drawHistoryRecords) : null;
              if (r && r.a && r.b && fwd.H15_ShiftDiff) {
                  const mockPatterns = {
                      h15_val: String(fwd.H15_ShiftDiff),
                      h14_val: String(fwd.H14_PrefixDiff_615 || '000'),
                      h7_val:  String(fwd.H7_DiffDiffSum || '000')
                  };
                  const r1 = r.evalRule(r.a[0], mockPatterns);
                  const r2 = r.evalRule(r.b[0], mockPatterns);
                  fwdCodes += `<br><span class="text-[10px] text-pink-700 font-bold bg-pink-50 px-1 py-0.5 rounded mt-1 inline-block">\U0001f52e Dynamic Master Formula Predicted AB: [${r1}${r2}] / [${r2}${r1}]</span>`;
              }
          } catch(e) {
              console.error(e);
          }
"""

content = re.sub(target, replacer, content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
