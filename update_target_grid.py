import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_injection = '''
              <div class="mt-4 p-3 bg-gradient-to-r from-slate-100 to-slate-200 border border-slate-300 rounded-lg shadow-inner">
                <div class="text-xs font-black text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-300 pb-1 flex items-center justify-between">
                  <span>🚀 ACTIVE BASELINE: <strong class="text-indigo-900">${activeBase}</strong> — NEXT DIRECT TARGETS</span>
                  <span class="text-[10px] bg-slate-800 text-white px-2 py-0.5 rounded">H15, H14, H7, H17, H16</span>
                </div>
                
                <div class="mb-3 p-2 bg-amber-50 border border-amber-200 rounded text-center shadow-sm">
                  <div class="text-[10px] font-black text-amber-900 uppercase">🔥 Derived AB Anchor Pair 🔥</div>
                  <div class="text-[11px] text-amber-800 font-medium mt-0.5">
                    Formed by combining the <strong>last digit of H15</strong> and <strong>last digit of H14</strong>
                  </div>
                  <div class="text-2xl font-black text-rose-600 font-mono mt-1 tracking-widest">
                    [${activeResult.h15_val[2]}${activeResult.h14_val[2]}]
                  </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H15 (Shift-Diff)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h15_val}</div>
                    <div class="text-[10px] font-bold text-rose-700 mt-0.5">Tail Digit: <span class="text-lg">[${activeResult.h15_val[2]}]</span></div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H14 (Prefix-Diff)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h14_val}</div>
                    <div class="text-[10px] font-bold text-rose-700 mt-0.5">Tail Digit: <span class="text-lg">[${activeResult.h14_val[2]}]</span></div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H7 (Star Diff-Sum)</div>
                    <div class="text-sm font-black text-slate-700 font-mono mt-0.5">${activeResult.h7_val}</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H17 (Sum-Diff-Keep)</div>
                    <div class="text-sm font-black text-slate-700 font-mono mt-0.5">${activeResult.h17_val}</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H16 (Twin-Echo)</div>
                    <div class="text-sm font-black text-slate-700 font-mono mt-0.5">${activeResult.h16_val}</div>
                  </div>
                </div>
              </div>

              <!-- TARGET PICKS GRID (8 CARDS) -->
'''

# we need to replace the old block we just injected.
# We will match from `<div class="mt-4 p-3 bg-gradient-to-r` to `<!-- TARGET PICKS GRID (8 CARDS) -->`
pattern = re.compile(r'<div class="mt-4 p-3 bg-gradient-to-r.*?<!-- TARGET PICKS GRID \(8 CARDS\) -->', re.DOTALL)
content = pattern.sub(new_injection.strip(), content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
