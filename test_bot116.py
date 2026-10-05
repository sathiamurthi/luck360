import io
content = io.open('index.html', 'r', encoding='utf-8').read().splitlines()
found = False
for line in content:
    if "container-daily-hottest-timeline" in line:
        found = True
        break
print("Found" if found else "NOT FOUND")
