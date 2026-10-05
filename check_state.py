import io
import traceback
import sys

def check():
    content = io.open('index.html', 'r', encoding='utf-8').read()
    print("hist occurrences:", content.count("if (typeof hist !== 'undefined' && hist && hist.length > 0) {"))
    print("activeBase occurrences:", content.count("let activeBase = '';"))
check()
