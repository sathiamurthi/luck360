import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

injection = '''
              <div class="mt-4 p-3 bg-gradient-to-r from-slate-100 to-slate-200 border border-slate-300 rounded-lg shadow-inner">
                <div class="text-xs font-black text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-300 pb-1 flex items-center justify-between">
                  <span>? ACTIVE BASELINE: <strong class="text-indigo-900">${activeBase}</strong> ? NEXT DIRECT TARGETS</span>
                  <span class="text-[10px] bg-slate-800 text-white px-2 py-0.5 rounded">H15, H14, H7, H17, H16</span>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H15 (Shift-Diff)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h15_val}</div>
                    <div class="text-[10px] font-bold text-indigo-700 mt-0.5">Pair AB: [${activeResult.h15_val.slice(0,2)}]</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H14 (Prefix-Diff)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h14_val}</div>
                    <div class="text-[10px] font-bold text-indigo-700 mt-0.5">Pair AB: [${activeResult.h14_val.slice(0,2)}]</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H7 (Star Diff-Sum)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h7_val}</div>
                    <div class="text-[10px] font-bold text-indigo-700 mt-0.5">Pair AB: [${activeResult.h7_val.slice(0,2)}]</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H17 (Sum-Diff-Keep)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h17_val}</div>
                    <div class="text-[10px] font-bold text-indigo-700 mt-0.5">Pair AB: [${activeResult.h17_val.slice(0,2)}]</div>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 text-center shadow-sm">
                    <div class="text-[9px] font-bold text-slate-500">H16 (Twin-Echo)</div>
                    <div class="text-sm font-black text-emerald-700 font-mono mt-0.5">${activeResult.h16_val}</div>
                    <div class="text-[10px] font-bold text-indigo-700 mt-0.5">Pair AB: [${activeResult.h16_val.slice(0,2)}]</div>
                  </div>
                </div>
              </div>

              <!-- TARGET PICKS GRID (8 CARDS) -->
'''

content = content.replace('<!-- TARGET PICKS GRID (8 CARDS) -->', injection)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
