import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
print("Keeping:")
for i in range(3002, 3006):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
print("\nDeleting:")
for i in range(3006, 3010):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
print("...")
for i in range(3166, 3173):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
