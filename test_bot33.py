import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
new_content = content[:3059] + content[3169:]
with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_content))
print("Deleted Second Ticket Parser!")
