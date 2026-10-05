import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "is3pmReflected" in content:
    idx = content.find("is3pmReflected")
    print("Found! " + content[max(0, idx-50):idx+50])
else:
    print("NOT FOUND is3pmReflected")
