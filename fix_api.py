import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_save = '''async function save() {
    const st = $('tk-status');
    if (!cur) { st.textContent = 'Enter the draw result first.'; return; }
    const rec = { id: Date.now(), date: $('tk-date').value, slot: +$('tk-slot').value, result: cur.res, cost: cur.c.cost, win: cur.c.win, net: cur.c.net,
      text: $('tk-text').value, rates: rates(), repeats: $('tk-rep').checked, breakdown: cur.c.rows };
    hist.push(rec); localStorage.setItem(KEY, JSON.stringify(hist)); draw();
    if (+$('tk-slot').value < 4) {
      $('tk-slot').value = String(+$('tk-slot').value + 1);
      setTimeout(fromHistory, 100);
    }
    $('tk-res').value = ''; $('tk-text').value = ''; calc();
    try {
      const r = await fetch('/api/v1/tickets', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(rec) });
      st.textContent = r.ok ? 'Saved to DB and browser history.' : 'DB error; saved to browser only.';
    } catch (e) {
      st.textContent = 'DB error; saved to browser only.';
    }
  }'''

new_load = '''async function load() {
    try { hist = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { hist = []; }
    try {
      const r = await fetch('/api/v1/tickets');
      if (r.ok) {
        const j = await r.json();
        if (Array.isArray(j)) { hist = j; localStorage.setItem(KEY, JSON.stringify(j)); }
      }
    } catch (e) {}
    draw();
  }'''

# Replace save()
idx_save = content.find('async function save() {')
idx_save_end = content.find('Saved to browser history.\';\n  }', idx_save) + len('Saved to browser history.\';\n  }')
content = content[:idx_save] + new_save + content[idx_save_end:]

# Replace load()
idx_load = content.find('async function load() {')
idx_load_end = content.find('draw();\n  }', idx_load) + len('draw();\n  }')
content = content[:idx_load] + new_load + content[idx_load_end:]

# Replace the deletion inside draw()
old_del = '''hist = hist.filter(h => String(h.id) !== b.dataset.id); localStorage.setItem(KEY, JSON.stringify(hist));
      draw();'''
new_del = '''hist = hist.filter(h => String(h.id) !== b.dataset.id); localStorage.setItem(KEY, JSON.stringify(hist));
      try { await fetch('/api/v1/tickets/' + b.dataset.id, { method: 'DELETE' }); } catch(e){}
      draw();'''
content = content.replace(old_del, new_del)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
