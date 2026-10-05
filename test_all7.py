import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")
print(content[idx:idx+2500])
