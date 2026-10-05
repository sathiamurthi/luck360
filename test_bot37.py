import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "renderUpcomingSchedule" in line:
        print(f"renderUpcomingSchedule at {i+1}")
