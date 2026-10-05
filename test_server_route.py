import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
idx = content.find("/draw_history.json")
if idx != -1:
    div_start = content.rfind('@app.get', 0, idx)
    print(content[div_start:div_start+1000].encode('ascii', 'ignore').decode('ascii'))
