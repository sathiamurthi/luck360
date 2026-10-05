import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_fwd_logic = '''
          const fwd = item.next_generated_patterns || {};
          let fwdCodes = `H15: ${fwd.H15_ShiftDiff || '-'} | H14: ${fwd.H14_PrefixDiff_615 || '-'} | H7: ${fwd.H7_DiffDiffSum || '-'}`;
          
          let confs = [];
          const keys_to_check = {
             'H15': fwd.H15_ShiftDiff, 'H14': fwd.H14_PrefixDiff_615, 'H7': fwd.H7_DiffDiffSum,
             'H17': fwd.H17_SumDiffKeep, 'H16': fwd.H16_TwinEchoStep
          };
          let checked = new Set();
          for (let [k1, v1] of Object.entries(keys_to_check)) {
             if (!v1) continue;
             for (let [k2, v2] of Object.entries(keys_to_check)) {
                if (k1 === k2 || !v2 || checked.has(k2 + k1)) continue;
                checked.add(k1 + k2);
                
                if (v1 === v2) {
                   confs.push(`<span class="text-emerald-700 bg-emerald-50 px-1 border border-emerald-200 rounded">🔥 EXACT Target [${v1}] (${k1} & ${k2})</span>`);
                } else if (v1.slice(0,2) === v2.slice(0,2)) {
                   confs.push(`<span class="text-indigo-700 bg-indigo-50 px-1 border border-indigo-200 rounded">🎯 Front Pair AB [${v1.slice(0,2)}] (${k1} & ${k2})</span>`);
                } else if (v1[2] === v2[2]) {
                   confs.push(`<span class="text-rose-700 bg-rose-50 px-1 border border-rose-200 rounded">★ Last Digit [${v1[2]}] (${k1} & ${k2})</span>`);
                }
             }
          }
          if (confs.length > 0) {
             fwdCodes += `<div class="mt-1 flex flex-wrap gap-1 text-[9px] font-bold">` + confs.join('') + `</div>`;
          }
'''

# We need to replace:
#           const fwd = item.next_generated_patterns || {};
#           const fwdCodes = `H15: ${fwd.H15_ShiftDiff || '-'} | H14: ${fwd.H14_PrefixDiff_615 || '-'} | H7: ${fwd.H7_DiffDiffSum || '-'}`;
target_re = re.compile(r'          const fwd = item\.next_generated_patterns \|\| \{\};\s*const fwdCodes = `H15: \$\{fwd\.H15_ShiftDiff \|\| \'-\'\} \| H14: \$\{fwd\.H14_PrefixDiff_615 \|\| \'-\'\} \| H7: \$\{fwd\.H7_DiffDiffSum \|\| \'-\'\}`;')
content = target_re.sub(new_fwd_logic.strip(), content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
