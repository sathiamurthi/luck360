import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Cross-Day Generated Targets")
if idx != -1:
    print(content[max(0, idx+1500):idx+3500].encode('ascii', 'ignore').decode('ascii'))
