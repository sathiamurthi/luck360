import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("h15_val")
if idx != -1:
    div_start = content.rfind('const h15', 0, idx)
    print(content[div_start:div_start+500].encode('ascii', 'ignore').decode('ascii'))
