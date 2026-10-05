import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")
div_start = content.find("        `;", idx)
print(content[div_start:div_start+1500].encode('ascii', 'ignore').decode('ascii'))
