import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "tbody-upcoming-schedule" in content:
    print("Found tbody-upcoming-schedule in index.html")
else:
    print("NOT FOUND tbody-upcoming-schedule")
