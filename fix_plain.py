import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the plain generation logic
old_plain_logic = r"const plain = `Draw: \$\{sd\.nextLabel\} \(based on \$\{sd\.p\} -> \$\{sd\.c\}\)\\nAB : \$\{AB\.join\(' '\) \|\| '-'\}\\nBC : \$\{BC\.join\(' '\) \|\| '-'\}\\nAC : \$\{AC\.join\(' '\) \|\| '-'\}\\nABC: \$\{shown\.map\(a => a\.x\)\.join\(' '\) \|\| '-'\}`;"

new_plain_logic = r'''
      let abGroups = {};
      shown.forEach(a => {
         let ab = a.x.slice(0,2);
         if (!abGroups[ab]) abGroups[ab] = [];
         abGroups[ab].push(a.x);
      });
      let abGroupStr = `\n\nAB pair (first two digits), missing digit goes last\n`;
      abGroupStr += `AB pair | Already in the list | Missing-set numbers\n`;
      abGroupStr += `--------------------------------------------------------\n`;
      let sortedGroups = Object.keys(abGroups).sort((k1, k2) => abGroups[k2].length - abGroups[k1].length);
      sortedGroups.forEach(ab => {
         let present = abGroups[ab].sort();
         let missing = [];
         for(let i=0; i<=9; i++) {
            let cand = ab + i.toString();
            if (!present.includes(cand)) missing.push(cand);
         }
         abGroupStr += `${ab.padEnd(7)} | ${present.join(' ')} (${present.length})`.padEnd(45) + `| ${missing.join(', ')}\n`;
      });

      const plain = `Draw: ${sd.nextLabel} (based on ${sd.p} -> ${sd.c})\nAB : ${AB.join(' ') || '-'}\nBC : ${BC.join(' ') || '-'}\nAC : ${AC.join(' ') || '-'}\nABC: ${shown.map(a => a.x).join(' ') || '-'}` + abGroupStr;
'''

content = re.sub(old_plain_logic, new_plain_logic.strip(), content)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
