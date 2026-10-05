import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "date: tk-date.value" in line:
        print(f"{i+1}: {line}")
