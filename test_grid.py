import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "container-top-ab-pattern6" in content:
    idx = content.find("container-top-ab-pattern6")
    print("Found container-top-ab-pattern6 in index.html")
    print(content[idx:idx+500].encode('ascii', 'ignore').decode('ascii'))
