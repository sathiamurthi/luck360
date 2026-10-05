import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the corrupted block!
corrupted_str = '''
      // Populate TOP 7 RULES
      const top7Div = document.getElementById('top-7-rules');
      if (top7Div && hist && hist.length > 0) {
          const sortedHist = [...hist].sort((a,b) => { let d = new Date(a.date) - new Date(b.date); return d !== 0 ? d : a.slot - b.slot; });
          const topRules = findTopCombinations(sortedHist);
          top7Div.innerHTML = topRules.map((r, i) => `
            <div class="flex justify-between items-center text-[9px] font-sans font-medium text-slate-700">
              <span><span class="font-bold text-indigo-700">#${i+1}</span> ${r.rule}</span>
              <span class="bg-white px-1.5 py-0.5 rounded border border-slate-200 shadow-sm font-bold">${r.count} Hits</span>
            </div>
          `).join('');
      }
'''
content = content.replace(corrupted_str, '')

# Find the ACTUAL end of `bannerEl.innerHTML = \`...\`;`
# We know the block ends with `.join('');\n      }` or something like that.
# Let's search for the end of the template string and the `;`.
idx_end_of_banner = content.find('// 2. KERALA SCHEDULE')
if idx_end_of_banner != -1:
    content = content[:idx_end_of_banner] + corrupted_str + '\n      ' + content[idx_end_of_banner:]

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
