import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_box = """<div class="text-[9px] text-amber-900 font-medium mb-3">Formed by combining the last digit of H15 and last digit of H14</div>
          <div class="text-3xl font-black text-rose-600 tracking-[0.2em]">[ ${activeAB} ]</div>"""

new_box = """<div class="text-[9px] text-amber-900 font-medium mb-1">Anchor (H15.last + H14.last): <strong class="text-rose-600 text-sm">[ ${activeAB} ]</strong></div>
          <div class="w-full h-px bg-amber-200 my-2"></div>
          <div class="text-[10px] font-bold text-pink-700 tracking-wider mb-1 flex items-center gap-1 uppercase justify-center">
            <span class="text-xs">??</span> Master Formula Pair
          </div>
          <div class="text-[8px] text-pink-900 font-medium mb-2 leading-tight">R1: (H15 Mid + H14 Last) &nbsp;|&nbsp; R2: |H7 Last - H7 Mid|</div>
          <div class="text-2xl font-black text-pink-600 tracking-[0.1em]">
            [ ${(parseInt(activeResult.h15_val[1]) + parseInt(activeResult.h14_val[2])) % 10}${Math.abs(parseInt(activeResult.h7_val[2]) - parseInt(activeResult.h7_val[1]))} ] / [ ${Math.abs(parseInt(activeResult.h7_val[2]) - parseInt(activeResult.h7_val[1]))}${(parseInt(activeResult.h15_val[1]) + parseInt(activeResult.h14_val[2])) % 10} ]
          </div>"""

content = content.replace(old_box, new_box)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
