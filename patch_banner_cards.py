import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""              <p class="text-xs text-slate-800 font-medium font-sans leading-relaxed">
                <strong>Dual Confluence \+ Blind, 2 Additional Patterns &amp; Previous \$\{t1_tail\} Cycle:</strong> Applied across \$\{baseSlot\} winning ticket <strong>\$\{activeVal\}</strong> \(Head <strong>\$\{a_h\}</strong>, Tail <strong>\$\{a_t\}</strong>\) and previous result <strong>\$\{t1_tail\}</strong>\. 
                Your discovered <strong>Star H17</strong> on Tail \$\{a_t\} yields <strong>\$\{t2_val\} \\u2605</strong>! 
                Head H8 \+ <strong>Tail Blind T2</strong> converge on <strong>\$\{t1_val\} \\u2605</strong>, and <strong>\\u2605 Star H9 on Head \$\{a_h\}</strong> yields <strong>\$\{t3_val\} \\u2605</strong>\. 
                From previous <strong>\$\{t1_tail\}</strong>, the bypass leap delivers <strong>\$\{t4_val_target\} \\u2605</strong>, while H17 on \$\{t1_tail\} yields <strong>\$\{t6_val\} \\u2605</strong>, locking Front-Twin <strong>\$\{t6_val\.slice\(0,2\)\}</strong> alongside Head Blind T4 <strong>\$\{t5_val\} \\u2605</strong> and H15 <strong>\$\{t8_val\} \\u2605</strong>\.
              </p>"""

replacement = """              <div id="dynamic-4-subcards" class="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
                <!-- 4 subcards injected here by JS below -->
              </div>"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
else:
    print("Could not find paragraph target")

target2 = r"""              </div>
            `;
        \}
"""

replacement2 = """              </div>
            `;
            
            // INJECT 4 SUBCARDS
            const cardsContainer = document.getElementById('dynamic-4-subcards');
            if (cardsContainer && typeof drawHistoryRecords !== 'undefined' && drawHistoryRecords.length >= 4) {
                const latestDate = drawHistoryRecords[drawHistoryRecords.length - 1].date;
                const todayDraws = drawHistoryRecords.filter(d => d.date === latestDate);
                
                const yestDraws = drawHistoryRecords.filter(d => d.date !== latestDate);
                const prev8PM = yestDraws.length > 0 ? yestDraws[yestDraws.length - 1] : drawHistoryRecords[0];
                
                const seq = [];
                seq.push(prev8PM);
                let drawsAdded = 0;
                todayDraws.forEach(d => { if (drawsAdded < 4) { seq.push(d); drawsAdded++; } });
                
                const slotNames = ['1:00 PM', '3:00 PM', '6:00 PM', '8:00 PM'];
                while (seq.length < 5) {
                    seq.push({
                        time: slotNames[seq.length - 1] || '8:00 PM',
                        ticket: 'PENDING',
                        tail: '???',
                        date: latestDate
                    });
                }
                
                let cardsHtml = '';
                for (let i = 1; i <= 4; i++) {
                    const bDraw = seq[i-1];
                    const cDraw = seq[i];
                    
                    const bExt = extractHeadAndTail(bDraw.ticket !== 'PENDING' ? bDraw.ticket : '50E 94406');
                    const bTail = bDraw.tail !== '???' ? bDraw.tail : bExt.tail;
                    const bHead = bExt.head;
                    
                    let bPats = { h17_val: '---', h15_val: '---' }, bBlind = { b1: '---', b4: '---' };
                    try { bPats = calculateSingleDrawPatterns(bTail); bBlind = calcBlindPatterns(bTail); } catch(e){}
                    
                    let cardStory = '';
                    if (cDraw.ticket === 'PENDING') {
                        cardStory = `<strong>Dual Confluence Projections &amp; Previous ${bTail} Cycle:</strong> Projections for upcoming <strong>${cDraw.time}</strong> draw based on previous result <strong>${bTail}</strong>. From previous <strong>${bTail}</strong>, the bypass leap delivers <strong>${bBlind.b1} \u2605</strong>, while H17 on ${bTail} yields <strong>${bPats.h17_val} \u2605</strong>, locking Front-Twin <strong>${bPats.h17_val.substring(0,2)}</strong> alongside Head Blind T4 <strong>${bBlind.b4} \u2605</strong> and H15 <strong>${bPats.h15_val} \u2605</strong>. Awaiting ${cDraw.time} result for confluence.`;
                    } else {
                        const cExt = extractHeadAndTail(cDraw.ticket);
                        const cTail = cExt.tail;
                        const cHead = cExt.head;
                        let cPats = { h17_val: '---' }, cHeadPats = { h9_val: '---' }, cBlind = { b2: '---' };
                        try { cPats = calculateSingleDrawPatterns(cTail); cHeadPats = calculateSingleDrawPatterns(cHead); cBlind = calcBlindPatterns(cTail); } catch(e){}
                        
                        cardStory = `<strong>Dual Confluence + Blind &amp; Previous ${bTail} Cycle:</strong> Applied across <strong>${cDraw.time}</strong> winning ticket <strong>${cDraw.ticket}</strong> (Head <strong>${cHead}</strong>, Tail <strong>${cTail}</strong>) and previous result <strong>${bTail}</strong>. Your discovered <strong>Star H17</strong> on Tail ${cTail} yields <strong>${cPats.h17_val} \u2605</strong>! Head H8 + <strong>Tail Blind T2</strong> converge on <strong>${cBlind.b2} \u2605</strong>, and <strong>\u2605 Star H9 on Head ${cHead}</strong> yields <strong>${cHeadPats.h9_val} \u2605</strong>. From previous <strong>${bTail}</strong>, the bypass leap delivers <strong>${bBlind.b1} \u2605</strong>, while H17 on ${bTail} yields <strong>${bPats.h17_val} \u2605</strong>, locking Front-Twin <strong>${bPats.h17_val.substring(0,2)}</strong> alongside Head Blind T4 <strong>${bBlind.b4} \u2605</strong> and H15 <strong>${bPats.h15_val} \u2605</strong>.`;
                    }
                    
                    cardsHtml += `
                        <div class="bg-white/80 border border-amber-300 rounded-lg p-2.5 shadow-sm">
                            <div class="text-[10px] font-black text-amber-900 border-b border-amber-200 pb-1 mb-1.5 uppercase tracking-wide flex items-center justify-between">
                                <span>${bDraw.time.replace(' PM','')} \u2192 ${cDraw.time.replace(' PM','')} Transition</span>
                                <span class="bg-amber-100 px-1.5 py-0.5 rounded text-[9px] border border-amber-300">${cDraw.ticket === 'PENDING' ? 'PENDING TARGET' : 'PROVED'}</span>
                            </div>
                            <p class="text-[10.5px] text-slate-800 font-medium font-sans leading-snug">
                                ${cardStory}
                            </p>
                        </div>
                    `;
                }
                cardsContainer.innerHTML = cardsHtml;
            }
        }
"""

if re.search(target2, content):
    content = re.sub(target2, replacement2, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched banner into 4 subcards!")
else:
    print("Target 2 not found")
