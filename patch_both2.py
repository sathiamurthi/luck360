import io

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

start_marker = "let activeVal = '';"
end_marker = "a_t = headTailBase.tail;"
idx1 = content.find(start_marker)
idx2 = content.find(end_marker, idx1)

if idx1 != -1 and idx2 != -1:
    before = content[:idx1]
    after = content[idx2 + len(end_marker):]
    
    # We need to also remove the dynamic_prev_tail block that comes after a_t = headTailBase.tail;
    # It ends with `dynamic_prev_tail = '053';\n        }`
    end_marker2 = "dynamic_prev_tail = '053';\n        }"
    idx3 = after.find(end_marker2)
    if idx3 != -1:
        after = after[idx3 + len(end_marker2):]
    
    replacement_banner = """let activeVal = '';
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
            if (is8PMComplete) {
                baseSlot = '8 PM'; activeVal = val4; nextSlotNameStr = 'Tomorrow 1:00 PM (Dear Day)';
                dynamic_prev_tail = (t3 && t3 !== 'Pending') ? t3 : ((t2 && t2 !== 'Pending') ? t2 : (t1 || '053'));
            } else if (is6PMComplete) {
                baseSlot = '6 PM'; activeVal = val3; nextSlotNameStr = 'Tonight 8:00 PM (Dear Seagull)';
                dynamic_prev_tail = (t2 && t2 !== 'Pending') ? t2 : (t1 || '053');
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

    content = before + replacement_banner + after
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched Banner via slice")
else:
    print("Could not find banner block")
