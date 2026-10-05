import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                          <div class="flex justify-between items-center border-b border-amber-200 pb-1 text-\[9\.5px\]">
                              <span class="font-bold text-indigo-800">Tail H17: <span class="font-black text-indigo-950">\$\{cPats\.h17_val\}</span></span>
                              <span class="font-bold text-indigo-800">H15: <span class="font-black text-indigo-950">\$\{cPats\.h15_val\}</span></span>
                              <span class="font-bold text-indigo-800">H14: <span class="font-black text-indigo-950">\$\{cPats\.h14_val \|\| '---'\}</span></span>
                          </div>"""

if re.search(target, content):
    print("Found it!")
else:
    print("Not found.")
