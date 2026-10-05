import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""        // NEW: Absolute Subtraction Card
        let tailA = '000', tailB = '000';
        if \(is8PMComplete\) \{ tailA = t3 \|\| '626'; tailB = t4_val \|\| '406'; \}
        else if \(is6pmReflected\) \{ tailA = t2 \|\| '226'; tailB = t3 \|\| '626'; \}
        else if \(is3pmReflected\) \{ tailA = t1 \|\| '051'; tailB = t2 \|\| '226'; \}
        else if \(is1pmReflected\) \{ tailA = '406'; tailB = t1 \|\| '051'; \} // Fallback to prev day 8PM"""

replacement = """        // NEW: Absolute Subtraction Card
        let tailA = '000', tailB = '000';
        const vT = (v) => v && v.length === 3 && v !== 'Pending' ? v : null;
        
        const validLiveDraws = [];
        if (vT(t1)) validLiveDraws.push(t1);
        if (vT(t2)) validLiveDraws.push(t2);
        if (vT(t3)) validLiveDraws.push(t3);
        if (vT(t4)) validLiveDraws.push(t4);
        
        if (validLiveDraws.length >= 2) {
            tailB = validLiveDraws[validLiveDraws.length - 1]; // Current
            tailA = validLiveDraws[validLiveDraws.length - 2]; // Previous
        } else if (validLiveDraws.length === 1) {
            tailB = validLiveDraws[0];
            tailA = '406'; // Prev day fallback
        }"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched subtraction card to use live inputs robustly!")
else:
    print("Could not find the target to patch the subtraction card.")
