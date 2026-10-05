import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
idx = content.find("def get_script():")
print(content[max(0, idx-200):idx+200].encode('ascii', 'ignore').decode('ascii'))
