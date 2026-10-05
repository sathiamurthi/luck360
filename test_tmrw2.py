import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("slot: 'Tomorrow 1 PM'")
print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
