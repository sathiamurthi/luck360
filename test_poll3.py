import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("updateSlotUI")
print(content[idx+800:idx+2000].encode('ascii', 'ignore').decode('ascii'))
