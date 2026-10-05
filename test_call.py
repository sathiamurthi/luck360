import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("typeof renderUpcomingSchedule")
if idx != -1:
    print(content[max(0, idx-100):idx+200].encode('ascii', 'ignore').decode('ascii'))
