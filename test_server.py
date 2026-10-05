import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
if 'script1.js' in content:
    print("Found script1.js in luck360_api_server.py")
else:
    print("Not found in server code. How does it serve static files?")
