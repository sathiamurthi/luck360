import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()
for i, line in enumerate(content):
    if "async function loadComprehensiveReport()" in line:
        print(f"{i+1}: {line.strip()}")
