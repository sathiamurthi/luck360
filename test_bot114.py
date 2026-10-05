import io
import re
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
content = content.replace('console.log("Live poll waiting...", err);', 'console.log("Live poll waiting...", err); document.body.innerHTML = "<div style=\'color:red; font-size:20px; padding: 20px;\'><h1>POLL ERROR</h1><p>" + err.toString() + "</p><p>" + err.stack + "</p></div>" + document.body.innerHTML;')
with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(content)
