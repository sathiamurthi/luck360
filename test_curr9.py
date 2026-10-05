import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("ACCUMULATIVE HOTTEST RECOMMENDATIONS")
if idx != -1:
    missing_code = content[idx - 50:]
    with io.open('scratch/missing.js', 'w', encoding='utf-8') as f:
        f.write(missing_code)
    print("Saved missing code! length:", len(missing_code))
else:
    print("Not found")
