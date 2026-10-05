import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "schedule-header-title" in content:
    print("Found schedule-header-title in index.html")
