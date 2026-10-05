import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""        let dynamic_prev_tail = t1 \|\| '053';
        if \(typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords\.length >= 2\) \{
            const validD = drawHistoryRecords\.filter\(x => x\.tail && x\.tail\.length === 3\);
            if \(validD\.length >= 2\) \{
                dynamic_prev_tail = validD\[validD\.length - 2\]\.tail;
            \}
        \}"""

replacement = """        let dynamic_prev_tail = '053';
        const isValidT = (v) => v && v.length === 3 && v !== 'Pending';
        if (is8PMComplete) {
            dynamic_prev_tail = isValidT(t3) ? t3 : (isValidT(t2) ? t2 : (isValidT(t1) ? t1 : '053'));
        } else if (is6PMComplete) {
            dynamic_prev_tail = isValidT(t2) ? t2 : (isValidT(t1) ? t1 : '053');
        } else if (is3pmReflected) {
            dynamic_prev_tail = isValidT(t1) ? t1 : '053';
        } else if (is1pmReflected) {
            dynamic_prev_tail = '406'; // Previous day fallback
        } else {
            dynamic_prev_tail = '053';
        }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched dynamic_prev_tail to rely on live inputs!")
else:
    print("Could not find the target to patch the dynamic previous result.")
