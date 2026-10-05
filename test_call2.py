import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "pollLiveDatabase();" in content:
    print("Yes, pollLiveDatabase is called.")
