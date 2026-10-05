import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
idx = content.find("def get_draw_history")
print(content[idx:idx+800].encode('ascii', 'ignore').decode('ascii'))
