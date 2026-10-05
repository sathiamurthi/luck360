import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

marker = "timelineContainer.innerHTML = slots.map"
idx = content.find(marker)
if idx != -1:
    end_idx = content.find("        `).join('');", idx)
    if end_idx != -1:
        # We found the EXACT end of the timelineContainer block!
        # The replacement should go right after the join('');
        # Let's see what is after join('');
        after_idx = end_idx + len("        `).join('');")
        
        replacement = """        `).join('');

        // NEW: Absolute Subtraction Card
        let tailA = '000', tailB = '000';
        if (is8PMComplete) { tailA = t3 || '626'; tailB = t4_val || '406'; }
        else if (is6pmReflected) { tailA = t2 || '226'; tailB = t3 || '626'; }
        else if (is3pmReflected) { tailA = t1 || '051'; tailB = t2 || '226'; }
        else if (is1pmReflected) { tailA = '406'; tailB = t1 || '051'; } // Fallback to prev day 8PM

        const diff = Math.abs(parseInt(tailA) - parseInt(tailB));
        const subStr = String(diff).padStart(3, '0');
        const d1 = parseInt(subStr[0]), d2 = parseInt(subStr[1]), d3 = parseInt(subStr[2]);
        const subH15 = `${(d2 + 1) % 10}${(d3 - d1 + 10) % 10}${d1}`;
        const subH17 = `${(d1 + d2) % 10}${(d1 - d2 + 10) % 10}${d3}`;

        timelineContainer.innerHTML += `
          <div class="theme-card-inner border border-purple-300 bg-purple-50/40 rounded-xl p-3.5 shadow-sm space-y-2 font-mono text-xs mt-3 mb-3">
            <div class="flex justify-between items-center border-b border-purple-200 pb-1.5">
              <span class="font-extrabold text-purple-900">Absolute Subtraction (Last 2 Results)</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] border bg-purple-100 text-purple-800 font-extrabold border-purple-300">\uD83D\uDD2E DYNAMIC PATTERN</span>
            </div>
            <div class="text-[11px] text-purple-700 truncate font-sans font-bold">Base Tails: ${tailA} &amp; ${tailB}</div>
            <div class="text-[10px] text-purple-600 font-sans flex items-center gap-2">
              <span>Absolute Difference: |${tailA} - ${tailB}| = </span>
              <strong class="text-purple-900 font-mono text-sm bg-purple-100 px-1.5 py-0.5 rounded border border-purple-200">${subStr}</strong>
            </div>
            <div class="bg-white p-2 rounded-lg border border-purple-200 shadow-sm space-y-1">
              <div class="text-[10px] font-bold text-purple-500 uppercase">Generated Targets:</div>
              <div class="font-black text-indigo-800 text-xs tracking-wider flex justify-around">
                <span>Target H15: <strong class="text-rose-600">${subH15} \u2605</strong></span>
                <span>Target H17: <strong class="text-rose-600">${subH17} \u2605</strong></span>
              </div>
              <div class="text-[10px] text-purple-700 font-bold border-t border-purple-100 mt-1.5 pt-1.5">
                Top AB: ${subH15.substring(0,2)}, ${subH17.substring(0,2)} | Secondary: ${subH15.substring(1,3)}, ${subH17.substring(1,3)}
              </div>
            </div>
          </div>
        `;"""
        
        new_content = content[:end_idx] + replacement + content[after_idx:]
        with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
            f.write(new_content)
        print("Safely injected Subtraction Card ONCE!")
    else:
        print("Could not find end of timeline container.")
else:
    print("Could not find timeline container start.")
