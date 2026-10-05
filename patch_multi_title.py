import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""              let multiplierHtml = `
                  <div class="bg-pink-50 border border-pink-200 rounded p-1\.5 mt-1\.5 text-\[8\.5px\] font-mono text-pink-900 space-y-0\.5">
                      <div class="font-black text-pink-700 uppercase tracking-widest mb-1 pb-1 border-b border-pink-200">Next Result Guess \(N-2 &times; N-1\)</div>"""

replacement = """              let guessTitle = cDraw.ticket === 'PENDING' ? 'Next Result Prediction' : 'Current Result Prediction';
              let multiplierHtml = `
                  <div class="bg-pink-50 border border-pink-200 rounded p-1.5 mt-1.5 text-[8.5px] font-mono text-pink-900 space-y-0.5">
                      <div class="font-black text-pink-700 uppercase tracking-widest mb-1 pb-1 border-b border-pink-200">${guessTitle} (From Prev 2 Draws)</div>"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched title successfully!")
else:
    print("Target block not found.")
