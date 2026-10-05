import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("banner-hottest-recommendations")
print(content[idx:idx+2000].encode('ascii', 'ignore').decode('ascii'))
