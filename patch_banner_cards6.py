import io

content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(content):
    if "let cardStory = '';" in line:
        start_idx = i
    if start_idx != -1 and "cardsContainer.innerHTML = cardsHtml;" in line:
        end_idx = i
        break

replacement = """              let bHeadPats = { h17_val: '---', h15_val: '---' };
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
                  let cPats = { h17_val: '---', h15_val: '---' }, cHeadPats = { h17_val: '---', h15_val: '---' };
                  try { cPats = calculateSingleDrawPatterns(cTail); cHeadPats = calculateSingleDrawPatterns(cHead); } catch(e){}
                  
                  cardStory = `
                      <div class="font-bold text-slate-800 text-[10.5px] pb-1 border-b border-amber-200 mb-1">
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
                  <div class="bg-white border border-amber-300 rounded-lg p-2.5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between">
                      <div class="text-[10px] font-black text-amber-900 border-b border-amber-200 pb-1 mb-1.5 uppercase tracking-wide flex items-center justify-between">
                          <span>${bDraw.time.replace(' PM','')} \u2192 ${cDraw.time.replace(' PM','')} Transition</span>
                          <span class="${cDraw.ticket === 'PENDING' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'} px-1.5 py-0.5 rounded text-[9px] border ${cDraw.ticket === 'PENDING' ? 'border-amber-300' : 'border-emerald-300'}">${cDraw.ticket === 'PENDING' ? 'PENDING TARGET' : 'PROVED ALGORITHM'}</span>
                      </div>
                      <div class="font-sans leading-snug">
                          ${cardStory}
                      </div>
                  </div>
              `;
          }
          cardsContainer.innerHTML = cardsHtml;"""

if start_idx != -1 and end_idx != -1:
    content[start_idx:end_idx+1] = [replacement]
    with io.open('script1.js', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    print("Replaced dense text with structured rows successfully!")
else:
    print(f"Could not find block. start: {start_idx}, end: {end_idx}")
