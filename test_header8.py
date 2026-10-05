import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("Upcoming Guess Schedule")
print(content[max(0, idx-50):idx+150].encode('ascii', 'ignore').decode('ascii'))
