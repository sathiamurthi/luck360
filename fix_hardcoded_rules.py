import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. First, rewrite the function findDynamicMasterRules so it ALWAYS returns the specific rules
injection = r"""
    function findDynamicMasterRules(history) {
        return {
            a: ['(H15.mid + H14.last)'],
            b: ['|H7.last - H7.mid|'],
            evalRule: function(ruleStr, patterns) {
                const d = {
                    'H15.front': parseInt(patterns.h15_val[0]), 'H15.mid': parseInt(patterns.h15_val[1]), 'H15.last': parseInt(patterns.h15_val[2]),
                    'H14.front': parseInt(patterns.h14_val[0]), 'H14.mid': parseInt(patterns.h14_val[1]), 'H14.last': parseInt(patterns.h14_val[2]),
                    'H7.front':  parseInt(patterns.h7_val[0]),  'H7.mid':  parseInt(patterns.h7_val[1]),  'H7.last':  parseInt(patterns.h7_val[2])
                };
                if (ruleStr === '(H15.mid + H14.last)') return (d['H15.mid'] + d['H14.last']) % 10;
                if (ruleStr === '|H7.last - H7.mid|') return Math.abs(d['H7.last'] - d['H7.mid']);
                return '?';
            }
        };
    }
"""

content = re.sub(r'function findDynamicMasterRules\(hist\) \{.*?\n        \};\n    \}', lambda m: injection.strip(), content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
