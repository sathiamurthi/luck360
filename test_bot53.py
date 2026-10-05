import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

replacement = """    ['mp-prev', 'mp-curr'].forEach(id => { const el = $(id); if(el) el.addEventListener('input', render); });
    if($('mp-min')) $('mp-min').addEventListener('change', render); 
    if($('mp-gaps')) $('mp-gaps').addEventListener('change', render);
    if($('mp-sync')) $('mp-sync').addEventListener('click', sync);
    if($('mp-copy')) $('mp-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); if($('mp-status')) $('mp-status').textContent = 'Copied'; });
    if($('mp-banner-copy')) $('mp-banner-copy').addEventListener('click', () => { navigator.clipboard.writeText(window.__mpPlain || ''); if($('mp-banner-time')) $('mp-banner-time').textContent = 'copied'; });"""

new_content = content[:2907] + replacement.split('\n') + content[2912:]

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_content))

print("Patched mp- event listeners to be safe!")
