import io
# Read as bytes
with open('index.html', 'rb') as f:
    b = f.read()

# Try to decode as utf-8, replacing errors
try:
    content = b.decode('utf-8')
except UnicodeDecodeError:
    content = b.decode('utf-8', errors='replace')

# Write back as valid utf-8
with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))
