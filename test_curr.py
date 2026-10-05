import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "renderUpcomingSchedule" in content:
    print("Found renderUpcomingSchedule!")
else:
    print("NOT FOUND")
