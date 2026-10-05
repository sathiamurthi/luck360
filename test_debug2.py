import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx1 = content.find("function renderCrossSlotPatternTab")
idx2 = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")
print(f"renderCrossSlotPatternTab: {idx1}")
print(f"bannerEl: {idx2}")
