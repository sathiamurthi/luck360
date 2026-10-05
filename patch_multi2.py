import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()

target = r"""                      <div class="font-sans leading-snug">
                          \$\{cardStory\}
                      </div>
                  </div>
              `;"""

replacement = """                      <div class="font-sans leading-snug">
                          ${cardStory}
                          ${multiplierHtml}
                      </div>
                  </div>
              `;"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(content)
    print("Patched multiplierHtml into UI successfully!")
else:
    print("Target block not found.")
