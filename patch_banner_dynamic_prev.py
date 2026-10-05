import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"const t1_tail = t1 \|\| '053';\s*const t1_res = calculateSingleDrawPatterns\(t1_tail\);\s*const t1_blind = calcBlindPatterns\(t1_tail\);"

replacement = """        let dynamic_prev_tail = t1 || '053';
        if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length >= 2) {
            const validD = drawHistoryRecords.filter(x => x.tail && x.tail.length === 3);
            if (validD.length >= 2) {
                dynamic_prev_tail = validD[validD.length - 2].tail;
            }
        }
        const t1_tail = dynamic_prev_tail;
        const t1_res = calculateSingleDrawPatterns(t1_tail);
        const t1_blind = calcBlindPatterns(t1_tail);"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    
    # Also replace "1 PM" string literals in the text
    content = content.replace("and previous Dear 1 PM result", "and previous result")
    content = content.replace("From 1 PM <strong>", "From previous <strong>")
    content = content.replace("24-hour bypass leap", "bypass leap")
    content = content.replace("24H 1 PM DEAR BYPASS LEAP", "PREVIOUS DRAW BYPASS LEAP")
    content = content.replace("${t1_tail} 24H Cycle", "Previous ${t1_tail} Cycle")
    content = content.replace("${t1_tail} 24H PATTERNS", "PREV ${t1_tail} PATTERNS")
    
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched banner to use truly dynamic previous result instead of hardcoded 1 PM!")
else:
    print("Could not find the target to patch the dynamic previous result.")
