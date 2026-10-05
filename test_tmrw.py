import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Tomorrow 1 PM")
if idx != -1:
    print(content[max(0,idx-500):idx+1500].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found in script1.js")
