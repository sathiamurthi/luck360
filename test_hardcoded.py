import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("let drawHistoryRecords = [")
if idx != -1:
    print("Found hardcoded drawHistoryRecords")
    print(content[idx:idx+200].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
