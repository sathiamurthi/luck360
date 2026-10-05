import io
content = io.open('script1.js', 'r', encoding='utf-8').read()

new_func = r"""
    function renderUpcomingSchedule() {
        const tbody = document.getElementById('tbody-upcoming-schedule');
        if (!tbody || !drawHistoryRecords || drawHistoryRecords.length === 0) return;

        const latestDraw = drawHistoryRecords[drawHistoryRecords.length - 1];
        const latestDate = latestDraw.date || new Date().toISOString().split('T')[0];
        
        const headerTitle = document.getElementById('schedule-header-title');
        if (headerTitle) {
            headerTitle.innerHTML = `<span>\uD83D\uDD2E</span> Dynamic Daily Guess Schedule (From ${latestDate})`;
        }

        const recentDraws = drawHistoryRecords.slice(-5).reverse();
        let html = '';
        
        recentDraws.forEach(draw => {
            if (!draw.tail || draw.tail.length !== 3) return;
            const d1 = parseInt(draw.tail[0]);
            const d2 = parseInt(draw.tail[1]);
            const d3 = parseInt(draw.tail[2]);
            
            // H6 Target: (D1-D2, D1+D2+1, D3)
            const h6 = `${(d1 - d2 + 10) % 10}${(d1 + d2 + 1) % 10}${d3}`;
            
            // H2 Target: Cross-Swap
            const transMap58 = { 5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1 };
            const d2Trans = transMap58[d2] !== undefined ? transMap58[d2] : (d2 + 3) % 10;
            const h2 = `${(d1 + d2) % 10}${d3}${d2Trans}`;
            
            // H3 Target
            const h3 = `${(d1 - d2 + 10) % 10}${(d1 + d2 + d3) % 10}${(d1 - d3 + 10) % 10}`;
            
            // Pattern 1 Target
            const p1 = `${d3}${d2}${(d3 - d1 + 10) % 10}`;
            
            html += `<tr class="hover:bg-slate-50">
                <td class="py-3 px-4 font-bold text-slate-700">${draw.date || ''}</td>
                <td class="py-3 px-4 text-slate-900 font-bold">${draw.lottery || ''} ${draw.time || ''}</td>
                <td class="py-3 px-4 font-mono text-slate-600 font-bold">${draw.tail}</td>
                <td class="py-3 px-4 font-black text-emerald-700 text-base">${h6}</td>
                <td class="py-3 px-4 font-black text-amber-700 text-base">${h2}</td>
                <td class="py-3 px-4 font-black text-indigo-700 text-base">${h3}</td>
                <td class="py-3 px-4 font-bold text-teal-700">${p1}</td>
            </tr>`;
        });
        
        tbody.innerHTML = html;
    }
"""

idx_poll = content.find("renderCrossSlotPatternTab();")
if idx_poll != -1:
    content = content[:idx_poll+30] + "\n            if (typeof renderUpcomingSchedule === 'function') renderUpcomingSchedule();\n" + content[idx_poll+30:]
    content += "\n" + new_func + "\n"
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected renderUpcomingSchedule")
