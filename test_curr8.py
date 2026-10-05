import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
idx = content.find("        // 2. ACCUMULATIVE HOTTEST RECOMMENDATIONS THROUGHOUT THE DAY (1-DAY CYCLE PROGRESS)")
if idx != -1:
    missing_code = content[idx:]
    curr_script = io.open('script1.js', 'r', encoding='utf-8').read()
    # Find where to append!
    # script1.js currently ends somewhere.
    # Let's just append missing_code to the end of script1.js, BUT INSIDE the calculatePredictions function!
    # Wait, the bannerEl block was inside calculatePredictions()!
    # Let's check if the end of script1.js currently closes calculatePredictions!
    # No, we saw that it closed an IIFE at the end!
    print("Missing code length:", len(missing_code))
else:
    print("Not found")
