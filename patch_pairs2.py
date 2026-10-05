import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""              const getCrossPairs = \(pats\) => \{
                  if \(!pats \|\| !pats\.h15_val \|\| !pats\.h17_val\) return \[\];
                  const h15 = pats\.h15_val;
                  const h17 = pats\.h17_val;
                  if\(h15==='---' \|\| h17==='---'\) return \[\];
                  return \[\.\.\.new Set\(\[
                      h15\[2\] \+ h17\[2\],
                      h15\[2\] \+ h17\[0\],
                      h15\[0\] \+ h17\[2\],
                      h15\[0\] \+ h17\[0\]
                  \]\)\];
              \};"""

replacement = """              const getCrossPairs = (pats) => {
                  if (!pats || !pats.h15_val || !pats.h17_val) return [];
                  const h15 = pats.h15_val;
                  const h17 = pats.h17_val;
                  if(h15==='---' || h17==='---') return [];
                  return [...new Set([
                      h15[2] + h17[2],
                      h15[2] + h17[0],
                      h15[0] + h17[2],
                      h15[0] + h17[0],
                      h15[1] + h17[0],
                      h15[1] + h17[2]
                  ])];
              };"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched additional cross pairs successfully!")
else:
    print("Target block not found.")
