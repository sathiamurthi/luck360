import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
start_marker = "const bannerEl = document.getElementById('banner-hottest-recommendations');"
idx = content.find(start_marker)
print(content[idx:idx+2500])
