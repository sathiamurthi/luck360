import io
content = io.open('index.html', 'r', encoding='utf-8').read()

err_script = """
<script>
window.onerror = function(msg, url, lineNo, columnNo, error) {
  var errDiv = document.getElementById('debug-errors');
  if (!errDiv) {
    errDiv = document.createElement('div');
    errDiv.id = 'debug-errors';
    errDiv.style.cssText = 'position:fixed; top:0; left:0; width:100%; background:red; color:white; z-index:9999; padding:10px; font-family:monospace; font-size:12px;';
    document.body.prepend(errDiv);
  }
  errDiv.innerHTML += "<br>Error: " + msg + " at " + lineNo + ":" + columnNo;
  return false;
};
</script>
"""

content = content.replace('<head>', '<head>\n' + err_script)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected error logger!")
