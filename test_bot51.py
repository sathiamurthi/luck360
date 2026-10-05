import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

new_content = content[:2919] + content[3059:]

with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_content))

print("Deleted corrupted Ticket Parser block completely!")
