import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
count = content.count('function calculatePredictions')
print(f"calculatePredictions appears {count} times")
