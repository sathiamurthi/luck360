import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_logic = """
    function getCrossDayPools(history) {
        if (!history || history.length < 2) return null;
        let validDraws = history.filter(x => x.tail && x.tail.length === 3);
        if (validDraws.length < 2) return null;
        
        let latestDate = validDraws[validDraws.length - 1].date;
        let todaysDraws = validDraws.filter(x => x.date === latestDate);
        
        if (todaysDraws.length < 2) {
            let prevDate = validDraws.filter(x => x.date !== latestDate).pop()?.date;
            todaysDraws = validDraws.filter(x => x.date === latestDate || x.date === prevDate).slice(-4);
        }
        
        let pairs = new Set();
        let subDigits = new Set();
        
        const getSubs = (str) => {
            let res = [];
            for (let i = 0; i < str.length - 1; i++) {
                res.push(str.slice(i, i+2));
                res.push(str.slice(i, i+2).split('').reverse().join(''));
            }
            if (str.length >= 2) {
                res.push(str[0] + str[str.length-1]);
                res.push(str[str.length-1] + str[0]);
            }
            return res;
        };

        for (let i = 0; i < todaysDraws.length - 1; i++) {
            let t1 = todaysDraws[i].tail;
            let t2 = todaysDraws[i+1].tail;
            
            let v1 = parseInt(t1);
            let r1 = parseInt(t1.split('').reverse().join(''));
            let r2 = parseInt(t2.split('').reverse().join(''));
            
            let m1 = String(v1 * r2);
            let m2 = String(r1 * r2);
            
            getSubs(m1).forEach(p => pairs.add(p));
            getSubs(m2).forEach(p => pairs.add(p));
            
            let s = String(Math.abs(parseInt(t1) - parseInt(t2))).padStart(3, '0');
            s.split('').forEach(d => subDigits.add(d));
        }
        
        return { pairs: Array.from(pairs).sort(), subDigits: Array.from(subDigits).sort() };
    }
"""

if 'function getCrossDayPools' not in content:
    content = content.replace('function findTopCombinations', js_logic + '\n    function findTopCombinations')


# Find the active panel HTML to replace
start_anchor = '<div class="text-[10px] font-bold text-pink-700 uppercase flex items-center justify-center gap-1">'
end_anchor = '})()}</div>'
# Wait, let's just find the exact block.
# Let's see the current content block near the active result panel.
