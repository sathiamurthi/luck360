import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("function loadComprehensiveReport")
print(content[idx:idx+1000].encode('ascii', 'ignore').decode('ascii'))
