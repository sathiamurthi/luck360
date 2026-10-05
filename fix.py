# -*- coding: utf-8 -*-
import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '~.': '★',
    '?': '•',
    '^''': '→',
    '+''': '➔',
    'dY"': '🎯',
    'dY-': '🗑'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
