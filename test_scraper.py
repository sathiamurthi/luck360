import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
if "kerala" in content.lower():
    print("Kerala mentions in luck360_api_server.py")
