import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update findTopCombinations to support prev.tail
content = content.replace(
    'String(prev.result || "000")',
    'String(prev.result || prev.tail || "000")'
).replace(
    'String(curr.result || "000")',
    'String(curr.result || curr.tail || "000")'
)

pop_logic = '''
      // Populate TOP 7 RULES
      const top7Div = document.getElementById('top-7-rules');
      if (top7Div) {
          if (hist && hist.length > 0) {
              const sortedHist = [...hist].sort((a,b) => { let d = new Date(a.date) - new Date(b.date); return d !== 0 ? d : a.slot - b.slot; });
              const topRules = findTopCombinations(sortedHist);
              top7Div.innerHTML = topRules.map((r, i) => `
                <div class="flex justify-between items-center text-[9px] font-sans font-medium text-slate-700">
                  <span><span class="font-bold text-indigo-700">#${i+1}</span> ${r.rule}</span>
                  <span class="bg-white px-1.5 py-0.5 rounded border border-slate-200 shadow-sm font-bold">${r.count} Hits</span>
                </div>
              `).join('');
          } else {
              fetch('draw_history.json').then(r=>r.json()).then(hist2 => {
                  const sortedHist2 = [...hist2].sort((a,b) => { let d = new Date(a.date) - new Date(b.date); return d !== 0 ? d : (a.time.includes('1:00') ? 1 : (a.time.includes('3:00') ? 2 : (a.time.includes('6:00') ? 3 : 4))) - (b.time.includes('1:00') ? 1 : (b.time.includes('3:00') ? 2 : (b.time.includes('6:00') ? 3 : 4))); });
                  const topRules = findTopCombinations(sortedHist2);
                  top7Div.innerHTML = topRules.map((r, i) => `
                    <div class="flex justify-between items-center text-[9px] font-sans font-medium text-slate-700">
                      <span><span class="font-bold text-indigo-700">#${i+1}</span> ${r.rule}</span>
                      <span class="bg-white px-1.5 py-0.5 rounded border border-slate-200 shadow-sm font-bold">${r.count} Hits</span>
                    </div>
                  `).join('');
              });
          }
      }
'''

# Find the end of renderCrossSlotPatternTab()
idx = content.find('function syncCrossSlotInputs()')
# The `}` before this belongs to renderCrossSlotPatternTab
idx_insert = content.rfind('}', 0, idx)

content = content[:idx_insert] + pop_logic + '\n' + content[idx_insert:]

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
