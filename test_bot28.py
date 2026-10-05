import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content[2950:]):
    if line.strip() == '})();':
        print(f"Ends at {2950 + i + 1}")
