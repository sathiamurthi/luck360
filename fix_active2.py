import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find where activeBase is declared and replace it.
# Let's search for `let activeBase = is3pmReflected`
pattern = r"let activeBase = is3pmReflected.*?} else if \(is6PMComplete\) {.*?activeBase = t3 \|\| '626';\s*}"

new_logic = """
      let activeBase = '000';
      // Find the most recent draw in history
      if (typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length > 0) {
          const lastRec = drawHistoryRecords[drawHistoryRecords.length - 1];
          let t = String(lastRec.tail || '').replace(/\\D/g, '');
          if (t.length >= 3) activeBase = t.slice(-3);
          
          if (lastRec.time.includes('1:00')) nextDrawSlotName = 'Today 3:00 PM (Kerala)';
          else if (lastRec.time.includes('3:00')) nextDrawSlotName = 'Tonight 6:00 PM (Dear Mountain)';
          else if (lastRec.time.includes('6:00')) nextDrawSlotName = 'Tonight 8:00 PM (Dear Seagull)';
          else nextDrawSlotName = 'Tomorrow 1:00 PM (Dear Day)';
      } else {
          activeBase = t4_val || t3 || t2 || t1 || '000';
          nextDrawSlotName = 'Next Draw';
      }
"""

content = re.sub(pattern, new_logic.strip(), content, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
