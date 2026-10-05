import io

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""        const headTailBase = extractHeadAndTail(activeVal);
        a_h = headTailBase.head;
        a_t = headTailBase.tail;
        const t1_tail = dynamic_prev_tail;"""

replacement = """        const headTailBase = extractHeadAndTail(activeVal);
        a_h = headTailBase.head;
        a_t = headTailBase.tail;
        
        const headResultBase = calculateSingleDrawPatterns(a_h);
        const tailResultBase = calculateSingleDrawPatterns(a_t);
        const blindHeadBase = calcBlindPatterns(a_h);
        const blindTailBase = calcBlindPatterns(a_t);

        const t1_tail = dynamic_prev_tail;"""

if target in content:
    content = content.replace(target, replacement)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Fixed missing base variables!")
else:
    print("Could not find the target string to fix the missing variables.")
