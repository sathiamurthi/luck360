import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target = r"""                    let cardStory = '';
                    if \(cDraw\.ticket === 'PENDING'\) \{
                        cardStory = `<strong>Dual Confluence Projections &amp; Previous \$\{bTail\} Cycle:</strong> Projections for upcoming <strong>\$\{cDraw\.time\}</strong> draw based on previous result <strong>\$\{bTail\}</strong>\. From previous <strong>\$\{bTail\}</strong>, the bypass leap delivers <strong>\$\{bBlind\.b1\} </strong>, while H17 on \$\{bTail\} yields <strong>\$\{bPats\.h17_val\} </strong>, locking Front-Twin <strong>\$\{bPats\.h17_val\.substring\(0,2\)\}</strong> alongside Head Blind T4 <strong>\$\{bBlind\.b4\} </strong> and H15 <strong>\$\{bPats\.h15_val\} </strong>\. Awaiting \$\{cDraw\.time\} result for confluence\.`;
                    \} else \{
                        const cExt = extractHeadAndTail\(cDraw\.ticket\);
                        const cTail = cExt\.tail;
                        const cHead = cExt\.head;
                        let cPats = \{ h17_val: '---' \}, cHeadPats = \{ h9_val: '---' \}, cBlind = \{ b2: '---' \};
                        try \{ cPats = calculateSingleDrawPatterns\(cTail\); cHeadPats = calculateSingleDrawPatterns\(cHead\); cBlind = calcBlindPatterns\(cTail\); \} catch\(e\)\{\}
                        
                        cardStory = `<strong>Dual Confluence \+ Blind &amp; Previous \$\{bTail\} Cycle:</strong> Applied across <strong>\$\{cDraw\.time\}</strong> winning ticket <strong>\$\{cDraw\.ticket\}</strong> \(Head <strong>\$\{cHead\}</strong>, Tail <strong>\$\{cTail\}</strong>\) and previous result <strong>\$\{bTail\}</strong>\. Your discovered <strong>Star H17</strong> on Tail \$\{cTail\} yields <strong>\$\{cPats\.h17_val\} </strong>! Head H8 \+ <strong>Tail Blind T2</strong> converge on <strong>\$\{cBlind\.b2\} </strong>, and <strong> Star H9 on Head \$\{cHead\}</strong> yields <strong>\$\{cHeadPats\.h9_val\} </strong>\. From previous <strong>\$\{bTail\}</strong>, the bypass leap delivers <strong>\$\{bBlind\.b1\} </strong>, while H17 on \$\{bTail\} yields <strong>\$\{bPats\.h17_val\} </strong>, locking Front-Twin <strong>\$\{bPats\.h17_val\.substring\(0,2\)\}</strong> alongside Head Blind T4 <strong>\$\{bBlind\.b4\} </strong> and H15 <strong>\$\{bPats\.h15_val\} </strong>\.`;
                    \}
                    
                    cardsHtml \+= `
                        <div class="bg-white border border-amber-300 rounded-lg p-2\.5 shadow-sm hover:shadow-md transition-shadow">
                            <div class="text-\[10px\] font-black text-amber-900 border-b border-amber-200 pb-1 mb-1\.5 uppercase tracking-wide flex items-center justify-between">
                                <span>\$\{bDraw\.time\.replace\(' PM',''\)\}  \$\{cDraw\.time\.replace\(' PM',''\)\} Transition</span>
                                <span class="\$\{cDraw\.ticket === 'PENDING' \? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'\} px-1\.5 py-0\.5 rounded text-\[9px\] border \$\{cDraw\.ticket === 'PENDING' \? 'border-amber-300' : 'border-emerald-300'\}">\$\{cDraw\.ticket === 'PENDING' \? 'PENDING TARGET' : 'PROVED ALGORITHM'\}</span>
                            </div>
                            <p class="text-\[10\.5px\] text-slate-800 font-medium font-sans leading-relaxed">
                                \$\{cardStory\}
                            </p>
                        </div>
                    `;"""

replacement = """                    let bHeadPats = { h17_val: '---', h15_val: '---' };
                    try { bHeadPats = calculateSingleDrawPatterns(bHead); } catch(e){}
                    
                    let cardStory = '';
                    if (cDraw.ticket === 'PENDING') {
                        cardStory = `
                            <div class="font-bold text-slate-800 text-[10.5px] pb-1">
                                Awaiting <span class="text-indigo-900">${cDraw.time}</span> Result for Confluence
                            </div>
                            <div class="bg-slate-50 border border-slate-200 rounded p-1.5 space-y-1">
                                <div class="text-[9px] font-black text-slate-500 uppercase tracking-widest">Base Targets (From Prev ${bTail} &amp; ${bHead})</div>
                                <div class="flex justify-between items-center border-b border-slate-200 pb-1">
                                    <span class="font-bold text-amber-800">Tail H17: <span class="font-black text-amber-950">${bPats.h17_val}</span></span>
                                    <span class="font-bold text-amber-800">Tail H15: <span class="font-black text-amber-950">${bPats.h15_val}</span></span>
                                </div>
                                <div class="flex justify-between items-center pt-0.5">
                                    <span class="font-bold text-emerald-800">Head H17: <span class="font-black text-emerald-950">${bHeadPats.h17_val}</span></span>
                                    <span class="font-bold text-emerald-800">Head H15: <span class="font-black text-emerald-950">${bHeadPats.h15_val}</span></span>
                                </div>
                            </div>
                        `;
                    } else {
                        const cExt = extractHeadAndTail(cDraw.ticket);
                        const cTail = cExt.tail;
                        const cHead = cExt.head;
                        let cPats = { h17_val: '---', h15_val: '---' }, cHeadPats = { h17_val: '---', h15_val: '---' }, cBlind = { b2: '---' };
                        try { cPats = calculateSingleDrawPatterns(cTail); cHeadPats = calculateSingleDrawPatterns(cHead); cBlind = calcBlindPatterns(cTail); } catch(e){}
                        
                        cardStory = `
                            <div class="font-bold text-slate-800 text-[10.5px] pb-1">
                                Ticket: <span class="text-indigo-900">${cDraw.ticket}</span> (Head: ${cHead}, Tail: ${cTail})
                            </div>
                            
                            <div class="bg-slate-50 border border-slate-200 rounded p-1.5 space-y-1">
                                <div class="text-[9px] font-black text-slate-500 uppercase tracking-widest">Base Influences (From Prev ${bTail} &amp; ${bHead})</div>
                                <div class="flex justify-between items-center border-b border-slate-200 pb-1">
                                    <span class="font-bold text-amber-800">Tail H17: <span class="font-black text-amber-950">${bPats.h17_val}</span></span>
                                    <span class="font-bold text-amber-800">Tail H15: <span class="font-black text-amber-950">${bPats.h15_val}</span></span>
                                </div>
                                <div class="flex justify-between items-center pt-0.5">
                                    <span class="font-bold text-emerald-800">Head H17: <span class="font-black text-emerald-950">${bHeadPats.h17_val}</span></span>
                                    <span class="font-bold text-emerald-800">Head H15: <span class="font-black text-emerald-950">${bHeadPats.h15_val}</span></span>
                                </div>
                            </div>
                            
                            <div class="bg-amber-50 border border-amber-200 rounded p-1.5 space-y-1 mt-1.5">
                                <div class="text-[9px] font-black text-amber-700 uppercase tracking-widest">Generated Targets (From Curr ${cTail} &amp; ${cHead})</div>
                                <div class="flex justify-between items-center border-b border-amber-200 pb-1">
                                    <span class="font-bold text-indigo-800">Tail H17: <span class="font-black text-indigo-950">${cPats.h17_val}</span></span>
                                    <span class="font-bold text-indigo-800">Tail H15: <span class="font-black text-indigo-950">${cPats.h15_val}</span></span>
                                </div>
                                <div class="flex justify-between items-center pt-0.5">
                                    <span class="font-bold text-rose-800">Head H17: <span class="font-black text-rose-950">${cHeadPats.h17_val}</span></span>
                                    <span class="font-bold text-rose-800">Head H15: <span class="font-black text-rose-950">${cHeadPats.h15_val}</span></span>
                                </div>
                            </div>
                        `;
                    }
                    
                    cardsHtml += `
                        <div class="bg-white border border-amber-300 rounded-lg p-2.5 shadow-sm hover:shadow-md transition-shadow">
                            <div class="text-[10px] font-black text-amber-900 border-b border-amber-200 pb-1 mb-1.5 uppercase tracking-wide flex items-center justify-between">
                                <span>${bDraw.time.replace(' PM','')} \u2192 ${cDraw.time.replace(' PM','')} Transition</span>
                                <span class="${cDraw.ticket === 'PENDING' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'} px-1.5 py-0.5 rounded text-[9px] border ${cDraw.ticket === 'PENDING' ? 'border-amber-300' : 'border-emerald-300'}">${cDraw.ticket === 'PENDING' ? 'PENDING TARGET' : 'PROVED ALGORITHM'}</span>
                            </div>
                            <div class="font-sans leading-snug">
                                ${cardStory}
                            </div>
                        </div>
                    `;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched banner card text to grid format successfully!")
else:
    print("Target block not found. Checking if it's slightly different...")
