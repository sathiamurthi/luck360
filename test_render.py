import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("function renderUpcomingSchedule")
print(content[idx:idx+2500].encode('ascii', 'ignore').decode('ascii'))
