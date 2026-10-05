import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
content = content.replace('os.path.join(DB_DIR, "script1.js")', 'os.path.join(WORKSPACE_DIR, "script1.js")')
with io.open('luck360_api_server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed directory to WORKSPACE_DIR")
