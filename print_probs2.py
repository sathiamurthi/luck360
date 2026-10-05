import io
content = io.open('inject_probs.py', 'r', encoding='utf-8').read()
print(content.encode("ascii", "ignore").decode("ascii"))
