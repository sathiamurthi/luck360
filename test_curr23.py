import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
count = content.count('function pollLiveDatabase')
print(f"pollLiveDatabase appears {count} times")
