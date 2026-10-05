import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "$('tk-hist').innerHTML =" in line:
        print(f"$('tk-hist') at {i+1}: {line}")
