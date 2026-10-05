import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target_banner = r"""        let activeVal = '';
        let a_h = '944';
        let a_t = '406';
        let nextSlotNameStr = '';
        
        if \(is8PMComplete\) \{
            baseSlot = '8 PM'; activeVal = val4; nextSlotNameStr = 'Tomorrow 1:00 PM \(Dear Day\)';
        \} else if \(is6PMComplete\) \{
            baseSlot = '6 PM'; activeVal = val3; nextSlotNameStr = 'Tonight 8:00 PM \(Dear Seagull\)';
        \} else if \(is3pmReflected\) \{
            baseSlot = '3 PM'; activeVal = val2; nextSlotNameStr = 'Tonight 6:00 PM \(Sikkim State Lottery\)';
        \} else if \(is1pmReflected\) \{
            baseSlot = '1 PM'; activeVal = val1; nextSlotNameStr = 'Today 3:00 PM \(Kerala State\)';
        \} else \{
            baseSlot = '8 PM \(Prev\)'; activeVal = val4 \|\| '50E 94406'; nextSlotNameStr = 'Today 1:00 PM \(Dear Day\)';
        \}

        const headTailBase = extractHeadAndTail\(activeVal\);
        a_h = headTailBase\.head;
        a_t = headTailBase\.tail;

        let dynamic_prev_tail = '053';
        const isValidT = \(v\) => v && v\.length === 3 && v !== 'Pending';
        if \(is8PMComplete\) \{
            dynamic_prev_tail = isValidT\(t3\) \? t3 : \(isValidT\(t2\) \? t2 : \(isValidT\(t1\) \? t1 : '053'\)\);
        \} else if \(is6PMComplete\) \{
            dynamic_prev_tail = isValidT\(t2\) \? t2 : \(isValidT\(t1\) \? t1 : '053'\);
        \} else if \(is3pmReflected\) \{
            dynamic_prev_tail = isValidT\(t1\) \? t1 : '053';
        \} else if \(is1pmReflected\) \{
            dynamic_prev_tail = '406'; // Previous day fallback
        \} else \{
            dynamic_prev_tail = '053';
        \}"""

replacement_banner = """        let activeVal = '';
        let a_h = '944';
        let a_t = '406';
        let nextSlotNameStr = '';
        let dynamic_prev_tail = '053';
        
        let foundLatest = false;
        if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length >= 2) {
            const vD = drawHistoryRecords.filter(x => x.tail && x.tail.length === 3);
            if (vD.length >= 2) {
                const latest = vD[vD.length - 1];
                const prev = vD[vD.length - 2];
                baseSlot = latest.time.replace(':00', '');
                activeVal = latest.ticket;
                dynamic_prev_tail = prev.tail;
                
                if (baseSlot.includes('1 PM')) nextSlotNameStr = 'Today 3:00 PM (Kerala State)';
                else if (baseSlot.includes('3 PM')) nextSlotNameStr = 'Tonight 6:00 PM (Sikkim State Lottery)';
                else if (baseSlot.includes('6 PM')) nextSlotNameStr = 'Tonight 8:00 PM (Dear Seagull)';
                else nextSlotNameStr = 'Tomorrow 1:00 PM (Dear Day)';
                foundLatest = true;
            }
        }
        
        if (!foundLatest) {
            // Fallback for initial load before fetch completes
            if (is8PMComplete) {
                baseSlot = '8 PM'; activeVal = val4; nextSlotNameStr = 'Tomorrow 1:00 PM (Dear Day)';
                dynamic_prev_tail = t3 || t2 || t1 || '053';
            } else if (is6PMComplete) {
                baseSlot = '6 PM'; activeVal = val3; nextSlotNameStr = 'Tonight 8:00 PM (Dear Seagull)';
                dynamic_prev_tail = t2 || t1 || '053';
            } else if (is3pmReflected) {
                baseSlot = '3 PM'; activeVal = val2; nextSlotNameStr = 'Tonight 6:00 PM (Sikkim State Lottery)';
                dynamic_prev_tail = t1 || '053';
            } else if (is1pmReflected) {
                baseSlot = '1 PM'; activeVal = val1; nextSlotNameStr = 'Today 3:00 PM (Kerala State)';
                dynamic_prev_tail = '406';
            } else {
                baseSlot = '8 PM (Prev)'; activeVal = val4 || '50E 94406'; nextSlotNameStr = 'Today 1:00 PM (Dear Day)';
                dynamic_prev_tail = '053';
            }
        }

        const headTailBase = extractHeadAndTail(activeVal);
        a_h = headTailBase.head;
        a_t = headTailBase.tail;"""

if re.search(target_banner, content):
    content = re.sub(target_banner, replacement_banner, content)
    print("Patched Banner")
else:
    print("Banner target not found")

target_sub = r"""        // NEW: Absolute Subtraction Card
        let tailA = '000', tailB = '000';
        const vT = \(v\) => v && v\.length === 3 && v !== 'Pending' \? v : null;
        
        const validLiveDraws = \[\];
        if \(vT\(t1\)\) validLiveDraws\.push\(t1\);
        if \(vT\(t2\)\) validLiveDraws\.push\(t2\);
        if \(vT\(t3\)\) validLiveDraws\.push\(t3\);
        if \(vT\(t4\)\) validLiveDraws\.push\(t4\);
        
        if \(validLiveDraws\.length >= 2\) \{
            tailB = validLiveDraws\[validLiveDraws\.length - 1\]; // Current
            tailA = validLiveDraws\[validLiveDraws\.length - 2\]; // Previous
        \} else if \(validLiveDraws\.length === 1\) \{
            tailB = validLiveDraws\[0\];
            tailA = '406'; // Prev day fallback
        \}"""

replacement_sub = """        // NEW: Absolute Subtraction Card
        let tailA = '000', tailB = '000';
        
        if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length >= 2) {
            const vD = drawHistoryRecords.filter(x => x.tail && x.tail.length === 3);
            if (vD.length >= 2) {
                tailB = vD[vD.length - 1].tail; // Current
                tailA = vD[vD.length - 2].tail; // Previous
            }
        }
        
        if (tailA === '000' && tailB === '000') {
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
            }
        }"""

if re.search(target_sub, content):
    content = re.sub(target_sub, replacement_sub, content)
    print("Patched Sub")
else:
    print("Sub target not found")

with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
