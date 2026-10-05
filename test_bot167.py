import io
import traceback
import sys

def check_script():
    content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()
    # Let's write a node.js script to evaluate it and catch syntax errors
    # Wait, node isn't available. Let's use Microsoft JScript via cscript!
    with open('test.js', 'w', encoding='utf-8') as f:
        # We just want to check SYNTAX, not execute.
        # Unfortunately, cscript will execute it.
        pass

check_script()
print("Done")
