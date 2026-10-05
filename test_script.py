import io
content = io.open('index.html', 'r', encoding='utf-8').read()
if "<script>" in content:
    print("Found <script> in index.html")
