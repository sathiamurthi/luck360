import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("        // 2. ACCUMULATIVE HOTTEST RECOMMENDATIONS THROUGHOUT THE DAY")
if idx != -1:
    print("Found // 2. ACCUMULATIVE in script1.js")
else:
    print("NOT FOUND // 2. ACCUMULATIVE in script1.js")
