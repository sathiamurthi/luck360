import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("function getCrossDayTargets")
if idx != -1:
    print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
