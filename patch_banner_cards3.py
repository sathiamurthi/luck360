import io

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

target_p = """              <p class="text-xs text-slate-800 font-medium font-sans leading-relaxed">
                <strong>Dual Confluence + Blind, 2 Additional Patterns &amp; Previous ${t1_tail} Cycle:</strong> Applied across ${baseSlot} winning ticket <strong>${activeVal}</strong> (Head <strong>${a_h}</strong>, Tail <strong>${a_t}</strong>) and previous result <strong>${t1_tail}</strong>. 
                Your discovered <strong>Star H17</strong> on Tail ${a_t} yields <strong>${t2_val} \u2605</strong>! 
                Head H8 + <strong>Tail Blind T2</strong> converge on <strong>${t1_val} \u2605</strong>, and <strong>\u2605 Star H9 on Head ${a_h}</strong> yields <strong>${t3_val} \u2605</strong>. 
                From previous <strong>${t1_tail}</strong>, the bypass leap delivers <strong>${t4_val_target} \u2605</strong>, while H17 on ${t1_tail} yields <strong>${t6_val} \u2605</strong>, locking Front-Twin <strong>${t6_val.slice(0,2)}</strong> alongside Head Blind T4 <strong>${t5_val} \u2605</strong> and H15 <strong>${t8_val} \u2605</strong>.
              </p>"""

replacement_div = """              <div id="dynamic-4-subcards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-3 mt-3 mb-4">
                <!-- 4 subcards injected here by JS below -->
              </div>"""

if target_p in content:
    content = content.replace(target_p, replacement_div)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Replaced paragraph with grid div!")
else:
    print("Could not find exact paragraph.")
