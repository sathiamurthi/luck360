import io
import re

content = io.open('index.html', 'r', encoding='utf-8').read()

target = r'<script src="script1.js\?v=\d+"></script>'
replacement = """<script>
window.onerror = function(msg, url, line, col, error) {
    document.body.innerHTML = '<div style="color:red; font-size:20px; padding: 20px;"><h1>ERROR</h1><p>' + msg + '</p><p>Line: ' + line + ':' + col + '</p></div>' + document.body.innerHTML;
    return false;
};
window.addEventListener('unhandledrejection', function(event) {
    document.body.innerHTML = '<div style="color:red; font-size:20px; padding: 20px;"><h1>PROMISE ERROR</h1><p>' + event.reason + '</p></div>' + document.body.innerHTML;
});
</script>
<script src="script1.js?v=99991"></script>"""

if re.search(target, content):
    content = re.sub(target, replacement, content)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected error handler")
else:
    print("Could not find script tag in index.html")
