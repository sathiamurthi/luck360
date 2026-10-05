import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_draw_save = '''  function draw() {
    if (!hist.length) { tk-hist.innerHTML = '<p class="text-xs" style="color:var(--text-muted)">No saved tickets yet.</p>'; return; }
    const P = hist.reduce((a, h) => a + h.cost, 0), W = hist.reduce((a, h) => a + h.win, 0);
    tk-hist.innerHTML = <div class="text-sm font-extrabold pb-2">Played \ • Won \ • <span style="\">Balance \</span></div>
      <div class="overflow-x-auto"><table class="mp-tbl w-full"><thead><tr><th>Date</th><th>Draw</th><th>Result</th><th>Played</th><th>Won</th><th>P/L</th><th></th></tr></thead><tbody> +
      hist.slice().reverse().map((h, i) => {
        let details = 'No details saved.';
        if (h.breakdown && h.breakdown.length > 0) {
          details = h.breakdown.map(r => <div><b>\ \</b>: \ (₹\ -> ₹\)</div>).join('');
        }
        return <tr style="cursor:pointer" onclick="document.getElementById('det-\').classList.toggle('hidden')"><td>\</td><td>\</td><td class="font-black">\</td><td>\</td><td>\</td><td style="\">\</td><td><button data-id="\" class="tk-del text-xs">🗑</button></td></tr>
        <tr id="det-\" class="hidden bg-slate-50"><td colspan="7"><div class="p-2 text-[10px] space-y-1">\</div></td></tr>;
      }).join('') + '</tbody></table></div>';
    document.querySelectorAll('.tk-del').forEach(b => b.onclick = (e) => {
      e.stopPropagation();
      hist = hist.filter(h => String(h.id) !== b.dataset.id); localStorage.setItem(KEY, JSON.stringify(hist));
      draw();
    });
  }

  async function load() {
    try { hist = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { hist = []; }
    draw();
  }

  async function save() {
    const st = tk-status;
    if (!cur) { st.textContent = 'Enter the draw result first.'; return; }
    const rec = { id: Date.now(), date: tk-date.value, slot: +tk-slot.value, result: cur.res, cost: cur.c.cost, win: cur.c.win, net: cur.c.net,
      text: tk-text.value, rates: rates(), repeats: tk-rep.checked, breakdown: cur.c.rows };
    hist.push(rec); localStorage.setItem(KEY, JSON.stringify(hist)); draw();
    if (+tk-slot.value < 4) {
      tk-slot.value = String(+tk-slot.value + 1);
      setTimeout(fromHistory, 100);
    }
    tk-res.value = ''; tk-text.value = ''; calc();
    st.textContent = 'Saved to browser history.';
  }'''

# The previous replacement failed because my regex didn't match the current corrupted state.
# The corrupted state has: tk-status without quotes, no backticks, etc.
# But it DOES have 'Saved to browser history.'
# And it starts with unction draw() { 
idx1 = content.rfind('  function draw() {')
if idx1 != -1:
    idx2 = content.find('Saved to browser history.\';', idx1)
    if idx2 != -1:
        idx2_end = content.find('}', idx2) + 1
        content = content[:idx1] + new_draw_save + content[idx2_end:]

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
