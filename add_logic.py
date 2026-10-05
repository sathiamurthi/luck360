import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = '''
      // CUSTOM LOGIC: Find Top 7 Combinations for AB, BC, AC
      function findTopCombinations(history) {
          let counts = {};
          
          for (let i = 1; i < history.length; i++) {
              let prev = history[i-1];
              let curr = history[i];
              
              let prevTail = prev.tail.slice(-3);
              let currTail = curr.tail.slice(-3);
              
              let pats = calculateSingleDrawPatterns(prevTail);
              
              let ab = currTail.slice(0, 2);
              let bc = currTail.slice(1, 3);
              let ac = currTail[0] + currTail[2];
              
              const pKeys = [
                {k:'H15', v: pats.h15_val},
                {k:'H14', v: pats.h14_val},
                {k:'H7', v: pats.h7_val},
                {k:'H17', v: pats.h17_val},
                {k:'H16', v: pats.h16_val},
                {k:'H8', v: pats.h8_val},
                {k:'H9', v: pats.h9_val},
                {k:'H13', v: pats.h13_val},
                {k:'H18', v: pats.trans_val}, // mapped Trans_val to H18
                {k:'P1', v: pats.p1_val},
                {k:'P2', v: pats.p2_conv1},
                {k:'P3', v: pats.p3_val}
              ];
              
              for (let p1 of pKeys) {
                  for (let p2 of pKeys) {
                      if (!p1.v || !p2.v) continue;
                      
                      // Last Digits combo
                      let ldCombo = p1.v[2] + p2.v[2];
                      let fdCombo = p1.v[0] + p2.v[0];
                      
                      let inc = (key) => counts[key] = (counts[key] || 0) + 1;
                      
                      if (ldCombo === ab) inc(`Last Digits: ${p1.k} & ${p2.k} → AB`);
                      if (ldCombo === bc) inc(`Last Digits: ${p1.k} & ${p2.k} → BC`);
                      if (ldCombo === ac) inc(`Last Digits: ${p1.k} & ${p2.k} → AC`);
                      
                      if (fdCombo === ab) inc(`First Digits: ${p1.k} & ${p2.k} → AB`);
                      if (fdCombo === bc) inc(`First Digits: ${p1.k} & ${p2.k} → BC`);
                      if (fdCombo === ac) inc(`First Digits: ${p1.k} & ${p2.k} → AC`);
                  }
              }
          }
          
          let sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
          // Filter out duplicates like "H15 & H14" vs "H14 & H15"
          let seenPairs = new Set();
          let uniqueSorted = [];
          for (let [rule, count] of sorted) {
              if (count < 2) continue; // Must have hit at least twice
              
              let parts = rule.split(' → ');
              let condition = parts[0].split(': ')[1];
              let target = parts[1];
              let p1 = condition.split(' & ')[0];
              let p2 = condition.split(' & ')[1];
              
              let type = rule.includes('Last') ? 'Last' : 'First';
              
              let sig = [p1, p2].sort().join('-') + '-' + target + '-' + type;
              if (!seenPairs.has(sig)) {
                  seenPairs.add(sig);
                  uniqueSorted.push({ rule: `${type} Digits: ${p1} + ${p2} → ${target}`, p1, p2, target, type, count });
              }
          }
          
          return uniqueSorted.slice(0, 7);
      }
'''
content = content.replace('// CALCULATE BLIND PATTERNS', new_logic + '\n\n    // CALCULATE BLIND PATTERNS')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
