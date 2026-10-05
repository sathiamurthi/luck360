import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "container-top-ab-pattern6" in content:
    idx = content.find("container-top-ab-pattern6")
    print(content[idx:idx+500].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found in script1.js")
