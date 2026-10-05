import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'const sortedHist = [...hist].sort((a,b) => new Date(a.date) - new Date(b.date));',
    'const sortedHist = [...hist].sort((a,b) => { let d = new Date(a.date) - new Date(b.date); return d !== 0 ? d : a.slot - b.slot; });'
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
