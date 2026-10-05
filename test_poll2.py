import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("function pollLiveDatabase")
print(content[idx+800:idx+1600].encode('ascii', 'ignore').decode('ascii'))
