import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Cross-Day Generated Targets")
if idx != -1:
    div_start = content.rfind('<div class="flex-1 p-2 bg-pink-50', 0, idx)
    print(content[max(0, div_start):idx+2000].encode('ascii', 'ignore').decode('ascii'))
