import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""              const bExt = extractHeadAndTail\(bDraw\.ticket !== 'PENDING' \? bDraw\.ticket : '50E 94406'\);
              const bTail = bDraw\.tail !== '\?\?\?' \? bDraw\.tail : bExt\.tail;
              const bHead = bExt\.head;"""

replacement = """              const bExt = extractHeadAndTail(bDraw.ticket !== 'PENDING' ? bDraw.ticket : '50E 94406');
              const bTail = bDraw.tail !== '???' ? bDraw.tail : bExt.tail;
              const bHead = bExt.head;
              
              let bbTail = '000';
              if (drawHistoryRecords && bDraw.id) {
                  const bIdx = drawHistoryRecords.findIndex(d => d.id === bDraw.id);
                  if (bIdx > 0) {
                      const bbExt = extractHeadAndTail(drawHistoryRecords[bIdx-1].ticket);
                      bbTail = bbExt.tail;
                  } else {
                      bbTail = bTail;
                  }
              } else {
                  bbTail = bTail;
              }
              
              let v1 = parseInt(bbTail);
              let v2 = parseInt(bTail);
              let s_r1 = bbTail.split('').reverse().join('');
              let s_r2 = bTail.split('').reverse().join('');
              let r1 = parseInt(s_r1);
              let r2 = parseInt(s_r2);
              
              let m_dir = String(v1 * v2);
              let m_r1 = String(r1 * v2);
              let m_r2 = String(v1 * r2);
              let m_r3 = String(r1 * r2);
              
              let multiplierHtml = `
                  <div class="bg-pink-50 border border-pink-200 rounded p-1.5 mt-1.5 text-[8.5px] font-mono text-pink-900 space-y-0.5">
                      <div class="font-black text-pink-700 uppercase tracking-widest mb-1 pb-1 border-b border-pink-200">Next Result Guess (N-2 &times; N-1)</div>
                      <div class="flex justify-between items-center"><span>Direct: ${bbTail}&times;${bTail} = ${m_dir}</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_dir.slice(-3).padStart(3, '0')}</strong></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Curr: ${s_r1}&times;${bTail} = ${m_r1}</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r1.slice(-3).padStart(3, '0')}</strong></div>
                      <div class="flex justify-between items-center"><span>Prev &times; Rev Curr: ${bbTail}&times;${s_r2} = ${m_r2}</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r2.slice(-3).padStart(3, '0')}</strong></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Rev Curr: ${s_r1}&times;${s_r2} = ${m_r3}</span> <strong class="text-rose-700 text-[9.5px]">^ ${m_r3.slice(-3).padStart(3, '0')}</strong></div>
                  </div>
              `;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched bbTail logic successfully!")
else:
    print("Target block not found.")
