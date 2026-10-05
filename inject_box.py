import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "box-active-baseline" not in content:
    idx = content.find('<section id="container-cross-consensus"')
    if idx != -1:
        content = content[:idx] + '<div id="box-active-baseline" class="mb-6"></div>\n      ' + content[idx:]
        with io.open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Injected box-active-baseline into index.html")
