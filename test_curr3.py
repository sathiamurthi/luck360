import io
content = io.open('scratch/test_script.js', 'r', encoding='utf-8').read()
if "Derived AB" in content:
    print("Found in test_script.js")
else:
    print("Not found in test_script.js")
