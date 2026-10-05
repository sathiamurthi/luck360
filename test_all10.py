import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")
div_start = content.find("        } else {", idx)
idx2 = content.find("      //", div_start+100)
print(content[idx2:idx2+1500].encode('ascii', 'ignore').decode('ascii'))
