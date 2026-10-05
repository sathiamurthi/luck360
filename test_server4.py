import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
if "def get_script():" in content:
    print("Function exists")
else:
    print("Function missing")
