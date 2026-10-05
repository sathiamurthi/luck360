import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("updateSlotUI")
print(content[idx+2000:idx+3500].encode('ascii', 'ignore').decode('ascii'))
