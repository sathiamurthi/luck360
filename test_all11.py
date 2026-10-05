import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
if "pollLiveDatabase" in content:
    print("Found pollLiveDatabase!")
else:
    print("Not found")
