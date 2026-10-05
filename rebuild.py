import io
import re

content = io.open('index - v1.html', 'r', encoding='utf-8').read()
# Find the start of the script block
m = re.search(r'<script>', content)
if m:
    html_part = content[:m.start()]
    new_html = html_part + '\n  <script src="script1.js"></script>\n</body>\n</html>'
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Rebuilt index.html from index - v1.html without inline JS!")
