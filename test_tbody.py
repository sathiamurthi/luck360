import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("tbody-upcoming-schedule")
if idx != -1:
    print("Found tbody-upcoming-schedule")
    print(content[max(0, idx-100):idx+500].encode('ascii', 'ignore').decode('ascii'))
else:
    print("NOT FOUND tbody-upcoming-schedule")
