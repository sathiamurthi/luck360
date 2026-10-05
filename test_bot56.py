import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
idx = 2692 - 1

content[idx] = "if($('nr-p1')) $('nr-p1').addEventListener('input',drawCross); if($('nr-p2')) $('nr-p2').addEventListener('input',drawCross);"

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content))

print("Patched nr-p1 listeners!")
