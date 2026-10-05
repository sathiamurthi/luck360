import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("setInterval")
print(content[idx:idx+500].encode('ascii', 'ignore').decode('ascii'))
