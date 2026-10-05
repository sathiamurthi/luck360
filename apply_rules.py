import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to history table
old_history_logic = "derivedHtml += `H15: ${p.h15_val} | H14: ${p.h14_val} | H7: ${p.h7_val}<br>`;"
new_history_logic = """
derivedHtml += `H15: ${p.h15_val} | H14: ${p.h14_val} | H7: ${p.h7_val}<br>`;
const r1 = (parseInt(p.h15_val[1]) + parseInt(p.h14_val[2])) % 10;
const r2 = Math.abs(parseInt(p.h7_val[2]) - parseInt(p.h7_val[1]));
derivedHtml += `<span class="text-[10px] text-pink-700 font-bold">?? Master Formula Pair: [${r1}${r2}] / [${r2}${r1}]</span><br>`;
"""
content = content.replace(old_history_logic, new_history_logic.strip())

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
