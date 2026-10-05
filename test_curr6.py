import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
print(content[-500:].encode('ascii', 'ignore').decode('ascii'))
