import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
target = r"const today = \$\('mp-today'\);"
replacement = r"const today = $('mp-today');\n      if (!today) return;"
content = content.replace(target, replacement)

target2 = r"const gaps = \$\('mp-gaps'\)\.checked, minScore = \+\$\('mp-min'\)\.value;"
replacement2 = r"const gaps = $('mp-gaps')?.checked || false, minScore = +($('mp-min')?.value || 2);"
content = content.replace(target2, replacement2)

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
print("Safeguarded mp-gaps and mp-today in script1.js")
