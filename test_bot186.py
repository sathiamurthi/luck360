import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
in_func = False
for i, line in enumerate(content):
    if "function calculateSingleDrawPatterns" in line:
        in_func = True
    if in_func:
        if line.strip() == "return {" or "return {" in line:
            for j in range(i-20, i+15):
                 print(f"{j+1}: {content[j].strip().encode('ascii', 'ignore').decode('ascii')}")
            break
