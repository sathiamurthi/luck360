import io
content = io.open('index.html', 'r', encoding='utf-8', errors='surrogatepass').read()
import re
# Remove the error handler block entirely
content = re.sub(r'<script>\s*window\.onerror.*?<\/script>\s*', '', content, flags=re.DOTALL)
with io.open('index.html', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
print("Removed error handler from index.html")
