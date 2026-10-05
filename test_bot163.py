import io
import subprocess

with open('test_node.js', 'w', encoding='utf-8') as f:
    f.write("""
const document = { getElementById: () => ({ innerHTML: '' }), querySelectorAll: () => ({ forEach: () => {} }), addEventListener: () => {} };
const window = { addEventListener: () => {} };
const fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
const setInterval = () => {};
const setTimeout = () => {};
""")
    content = io.open('script1.js', 'r', encoding='utf-8').read()
    f.write(content)

try:
    res = subprocess.run(['node', 'test_node.js'], capture_output=True, text=True, check=True)
    print("Syntax is OK")
except subprocess.CalledProcessError as e:
    print("SYNTAX ERROR:")
    print(e.stderr)
