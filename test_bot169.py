import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
in_poll = False
for i, line in enumerate(content):
    if "async function pollLiveDatabase()" in line or "function pollLiveDatabase()" in line:
        in_poll = True
    if in_poll and "loadComprehensiveReport" in line:
        print(f"Called in pollLiveDatabase at line {i+1}")
    if in_poll and line.startswith("    }"):
        in_poll = False
