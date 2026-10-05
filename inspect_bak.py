import io
content = io.open('index.html.bak', 'r', encoding='utf-8').read()
idx = content.find("Derived AB Anchor Pair")
if idx != -1:
    print(content[max(0, idx-100):idx+500].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found in bak")
