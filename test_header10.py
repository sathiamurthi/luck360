import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "schedule-header-title" in content:
    print("Found schedule-header-title!")
    idx = content.find("schedule-header-title")
    print(content[idx:idx+150].encode('ascii', 'ignore').decode('ascii'))
else:
    print("NOT FOUND!")
