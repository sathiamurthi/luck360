import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""              let m_dir = String\(v1 \* v2\);
              let m_r1 = String\(r1 \* v2\);
              let m_r2 = String\(v1 \* r2\);
              let m_r3 = String\(r1 \* r2\);
              
              let guessTitle = cDraw\.ticket === 'PENDING' \? 'Next Result Prediction' : 'Current Result Prediction';
              let multiplierHtml = `
                  <div class="bg-pink-50 border border-pink-200 rounded p-1\.5 mt-1\.5 text-\[8\.5px\] font-mono text-pink-900 space-y-0\.5">
                      <div class="font-black text-pink-700 uppercase tracking-widest mb-1 pb-1 border-b border-pink-200">\$\{guessTitle\} \(From Prev 2 Draws\)</div>
                      <div class="flex justify-between items-center"><span>Direct: \$\{bbTail\}&times;\$\{bTail\} = \$\{m_dir\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_dir\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{extractHeadAndTail\(cDraw\.ticket\)\.tail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Curr: \$\{s_r1\}&times;\$\{bTail\} = \$\{m_r1\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r1\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{extractHeadAndTail\(cDraw\.ticket\)\.tail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Prev &times; Rev Curr: \$\{bbTail\}&times;\$\{s_r2\} = \$\{m_r2\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r2\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{extractHeadAndTail\(cDraw\.ticket\)\.tail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Rev Curr: \$\{s_r1\}&times;\$\{s_r2\} = \$\{m_r3\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r3\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{extractHeadAndTail\(cDraw\.ticket\)\.tail\}\)</span>` : ''\}</div></div>
                  </div>
              `;"""

replacement = """              let m_dir = String(v1 * v2);
              let m_r1 = String(r1 * v2);
              let m_r2 = String(v1 * r2);
              let m_r3 = String(r1 * r2);
              
              const extractPairs = (s) => {
                  if (!s || s.length < 2) return '';
                  const f = s[0];
                  const l = s[s.length-1];
                  const lM1 = (parseInt(l) - 1 + 10) % 10;
                  return [...new Set([
                      s.slice(-2),
                      s.slice(0, 2),
                      l + f,
                      f + l,
                      String(lM1) + f,
                      f + String(lM1)
                  ])].join(',');
              };
              
              let guessTitle = cDraw.ticket === 'PENDING' ? 'Next Result Prediction' : 'Current Result Prediction';
              let multiplierHtml = `
                  <div class="bg-pink-50 border border-pink-200 rounded p-1.5 mt-1.5 text-[8.5px] font-mono text-pink-900 space-y-0.5">
                      <div class="font-black text-pink-700 uppercase tracking-widest mb-1 pb-1 border-b border-pink-200">${guessTitle} (From Prev 2 Draws)</div>
                      <div class="flex justify-between items-center border-b border-pink-100 pb-0.5">
                          <span>Dir: ${bbTail}&times;${bTail} = ${m_dir}</span> 
                          <div><span class="text-[7px] text-pink-500 mr-1 tracking-tighter">[${extractPairs(m_dir)}]</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_dir.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div>
                      </div>
                      <div class="flex justify-between items-center border-b border-pink-100 pb-0.5">
                          <span>R&times;C: ${s_r1}&times;${bTail} = ${m_r1}</span> 
                          <div><span class="text-[7px] text-pink-500 mr-1 tracking-tighter">[${extractPairs(m_r1)}]</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r1.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div>
                      </div>
                      <div class="flex justify-between items-center border-b border-pink-100 pb-0.5">
                          <span>P&times;R: ${bbTail}&times;${s_r2} = ${m_r2}</span> 
                          <div><span class="text-[7px] text-pink-500 mr-1 tracking-tighter">[${extractPairs(m_r2)}]</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r2.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div>
                      </div>
                      <div class="flex justify-between items-center">
                          <span>R&times;R: ${s_r1}&times;${s_r2} = ${m_r3}</span> 
                          <div><span class="text-[7px] text-pink-500 mr-1 tracking-tighter">[${extractPairs(m_r3)}]</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r3.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div>
                      </div>
                  </div>
              `;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched pairs successfully!")
else:
    print("Target block not found.")
