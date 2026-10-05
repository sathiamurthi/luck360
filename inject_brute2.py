import io
import re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

injection = r"""
    function findDynamicMasterRules(hist) {
        if (!hist || hist.length < 2) return null;
        let pairs = [];
        for (let i = 0; i < hist.length - 1; i++) {
            const prev = hist[i];
            const next = hist[i+1];
            let ab = String(next.result || next.tail || "000").replace(/\D/g, '');
            if (ab.length >= 3) ab = ab.slice(-3, -1);
            else continue;
            
            let t = String(prev.result || prev.tail || "000").replace(/\D/g, '');
            if (t.length >= 3) t = t.slice(-3);
            const p = calculateSingleDrawPatterns(t);
            if (!p) continue;
            pairs.push({ ab: ab, h15: p.h15_val, h14: p.h14_val, h7:  p.h7_val });
        }
        
        pairs = pairs.slice(-15);
        let a_rules = {}, b_rules = {};
        
        pairs.forEach(pair => {
            const a = parseInt(pair.ab[0]);
            const b = parseInt(pair.ab[1]);
            const d = {
                'H15.front': parseInt(pair.h15[0]), 'H15.mid': parseInt(pair.h15[1]), 'H15.last': parseInt(pair.h15[2]),
                'H14.front': parseInt(pair.h14[0]), 'H14.mid': parseInt(pair.h14[1]), 'H14.last': parseInt(pair.h14[2]),
                'H7.front':  parseInt(pair.h7[0]),  'H7.mid':  parseInt(pair.h7[1]),  'H7.last':  parseInt(pair.h7[2])
            };
            let ma = new Set(), mb = new Set();
            for (let [k, v] of Object.entries(d)) {
                if (v === a) ma.add(k);
                if (v === b) mb.add(k);
            }
            const keys = Object.keys(d);
            for (let i=0; i<keys.length; i++) {
                for (let j=i; j<keys.length; j++) {
                    let k1 = keys[i], k2 = keys[j];
                    let v1 = d[k1], v2 = d[k2];
                    if ((v1 + v2) % 10 === a) ma.add(`(${k1} + ${k2})`);
                    if ((v1 + v2) % 10 === b) mb.add(`(${k1} + ${k2})`);
                    if (Math.abs(v1 - v2) === a) ma.add(`|${k1} - ${k2}|`);
                    if (Math.abs(v1 - v2) === b) mb.add(`|${k1} - ${k2}|`);
                }
            }
            ma.forEach(m => a_rules[m] = (a_rules[m] || 0) + 1);
            mb.forEach(m => b_rules[m] = (b_rules[m] || 0) + 1);
        });
        
        let sorted_a = Object.entries(a_rules).sort((x,y) => y[1] - x[1]);
        let sorted_b = Object.entries(b_rules).sort((x,y) => y[1] - x[1]);
        
        return {
            a: sorted_a.length ? sorted_a[0] : null,
            b: sorted_b.length ? sorted_b[0] : null,
            evalRule: function(ruleStr, patterns) {
                if (!ruleStr) return '?';
                const d = {
                    'H15.front': parseInt(patterns.h15_val[0]), 'H15.mid': parseInt(patterns.h15_val[1]), 'H15.last': parseInt(patterns.h15_val[2]),
                    'H14.front': parseInt(patterns.h14_val[0]), 'H14.mid': parseInt(patterns.h14_val[1]), 'H14.last': parseInt(patterns.h14_val[2]),
                    'H7.front':  parseInt(patterns.h7_val[0]),  'H7.mid':  parseInt(patterns.h7_val[1]),  'H7.last':  parseInt(patterns.h7_val[2])
                };
                if (d[ruleStr] !== undefined) return d[ruleStr];
                let m = ruleStr.match(/\((.*?)\s*\+\s*(.*?)\)/);
                if (m) return (d[m[1]] + d[m[2]]) % 10;
                m = ruleStr.match(/\|(.*?)\s*-\s*(.*?)\|/);
                if (m) return Math.abs(d[m[1]] - d[m[2]]);
                return '?';
            }
        };
    }
"""

content = re.sub(r'function findTopCombinations\(history\) \{', lambda m: injection.strip() + '\n\n    function findTopCombinations(history) {', content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
