import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
print(content[-2000:].encode('ascii', 'ignore').decode('ascii'))
