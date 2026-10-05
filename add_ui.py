import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

injection = '''
              <div class="mt-4 p-3 bg-gradient-to-r from-slate-100 to-slate-200 border border-slate-300 rounded-lg shadow-inner">
                <div class="text-xs font-black text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-300 pb-1 flex items-center justify-between">
                  <span>🚀 ACTIVE BASELINE: <strong class="text-indigo-900">${activeBase}</strong> — NEXT DIRECT TARGETS</span>
                  <span class="text-[10px] bg-slate-800 text-white px-2 py-0.5 rounded">H15, H14, H7, H17, H16</span>
                </div>
                
                <div class="mb-3 flex flex-col md:flex-row gap-2">
                  <div class="flex-1 p-2 bg-amber-50 border border-amber-200 rounded text-center shadow-sm">
                    <div class="text-[10px] font-black text-amber-900 uppercase">🔥 Derived AB Anchor Pair 🔥</div>
                    <div class="text-[11px] text-amber-800 font-medium mt-0.5">
                      Formed by combining the <strong>last digit of H15</strong> and <strong>last digit of H14</strong>
                    </div>
                    <div class="text-2xl font-black text-rose-600 font-mono mt-1 tracking-widest">
                      [${activeResult.h15_val[2]}${activeResult.h14_val[2]}]
                    </div>
                  </div>
                  <div class="flex-1 p-2 bg-indigo-50 border border-indigo-200 rounded shadow-sm text-left">
                    <div class="text-[10px] font-black text-indigo-900 uppercase mb-1 border-b border-indigo-200 pb-0.5">🏆 Top 7 Historical Anchor Rules</div>
                    <div class="space-y-0.5" id="top-7-rules">
                      <!-- Populated dynamically -->
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
'''

target_re = re.compile(r'<div class="mt-4 p-3 bg-gradient-to-r.*?<div class="grid grid-cols-2 md:grid-cols-5 gap-2">', re.DOTALL)
content = target_re.sub(injection.strip(), content)

# Now find where to populate it. We can do it right after bannerEl.innerHTML = ...
pop_logic = '''
      // Populate TOP 7 RULES
      const top7Div = document.getElementById('top-7-rules');
      if (top7Div && hist && hist.length > 0) {
          const sortedHist = [...hist].sort((a,b) => new Date(a.date) - new Date(b.date));
          const topRules = findTopCombinations(sortedHist);
          top7Div.innerHTML = topRules.map((r, i) => `
            <div class="flex justify-between items-center text-[9px] font-sans font-medium text-slate-700">
              <span><span class="font-bold text-indigo-700">#${i+1}</span> ${r.rule}</span>
              <span class="bg-white px-1.5 py-0.5 rounded border border-slate-200 shadow-sm font-bold">${r.count} Hits</span>
            </div>
          `).join('');
      }
'''
idx_end = content.find('<!-- TARGET PICKS GRID (8 CARDS) -->')
idx_after_banner = content.find('}', idx_end) # end of if (bannerEl)
content = content[:idx_after_banner] + pop_logic + content[idx_after_banner:]

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
