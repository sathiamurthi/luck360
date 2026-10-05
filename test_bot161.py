import io
import json
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

# Search for any unclosed brackets or syntax errors by attempting a simple parse?
# Or just check if `t1_tail` was used somewhere else?
print("Done")
