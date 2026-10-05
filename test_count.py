import io
content = io.open('index.html', 'r', encoding='utf-8').read()
print(content.count("tbody-upcoming-schedule"))
