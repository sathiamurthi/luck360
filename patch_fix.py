import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                      <div class="flex justify-between items-center"><span>Direct: \$\{bbTail\}&times;\$\{bTail\} = \$\{m_dir\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_dir\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{cTail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Curr: \$\{s_r1\}&times;\$\{bTail\} = \$\{m_r1\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r1\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{cTail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Prev &times; Rev Curr: \$\{bbTail\}&times;\$\{s_r2\} = \$\{m_r2\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r2\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{cTail\}\)</span>` : ''\}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Rev Curr: \$\{s_r1\}&times;\$\{s_r2\} = \$\{m_r3\}</span> <div><strong class="text-rose-700 text-\[9\.5px\]">\^ \$\{m_r3\.slice\(-3\)\.padStart\(3, '0'\)\}</strong> \$\{cDraw\.ticket !== 'PENDING' \? `<span class="text-\[7\.5px\] text-pink-500 ml-1">\(Act: \$\{cTail\}\)</span>` : ''\}</div></div>"""

replacement = """                      <div class="flex justify-between items-center"><span>Direct: ${bbTail}&times;${bTail} = ${m_dir}</span> <div><strong class="text-rose-700 text-[9.5px]">^ ${m_dir.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Curr: ${s_r1}&times;${bTail} = ${m_r1}</span> <div><strong class="text-rose-700 text-[9.5px]">^ ${m_r1.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div></div>
                      <div class="flex justify-between items-center"><span>Prev &times; Rev Curr: ${bbTail}&times;${s_r2} = ${m_r2}</span> <div><strong class="text-rose-700 text-[9.5px]">^ ${m_r2.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div></div>
                      <div class="flex justify-between items-center"><span>Rev Prev &times; Rev Curr: ${s_r1}&times;${s_r2} = ${m_r3}</span> <div><strong class="text-rose-700 text-[9.5px]">^ ${m_r3.slice(-3).padStart(3, '0')}</strong> ${cDraw.ticket !== 'PENDING' ? `<span class="text-[7.5px] text-pink-500 ml-1">(Act: ${extractHeadAndTail(cDraw.ticket).tail})</span>` : ''}</div></div>"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched cTail reference error successfully!")
else:
    print("Target block not found.")
