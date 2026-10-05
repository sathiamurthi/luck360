import io
import re

content = io.open('index.html', 'r', encoding='utf-8').read()

err_script = """<script>
window.addEventListener('error', function(e) {
  document.body.insertAdjacentHTML('afterbegin', '<div style="color:red;font-size:20px;padding:20px;background:#fee;z-index:9999;position:relative;"><h1>SYNTAX ERROR</h1><p>' + e.message + ' at ' + e.filename + ':' + e.lineno + '</p></div>');
});
</script>"""

if "<h1>SYNTAX ERROR</h1>" not in content:
    content = content.replace("<head>", "<head>\n" + err_script)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Syntax Error Catcher!")
else:
    print("Already injected.")
