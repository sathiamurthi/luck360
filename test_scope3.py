import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")
div_start = content.rfind('function', 0, idx)
print(content[div_start:div_start+150])
