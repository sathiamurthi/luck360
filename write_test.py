import subprocess
js_mock = """
const dom = require('jsdom');
const { JSDOM } = dom;
const html = `<html><body>
<div id="container-daily-hottest-timeline"></div>
</body></html>`;
const jsdom = new JSDOM(html);
global.window = jsdom.window;
global.document = jsdom.window.document;
global.localStorage = { getItem:()=>null, setItem:()=>{} };
global.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
global.navigator = { clipboard: { writeText: ()=>{} } };

try {
    require('./script1.js');
    console.log("No syntax errors at load time!");
    if (typeof window.render === 'function') {
        window.render();
    }
} catch (e) {
    console.error("ERROR CAUGHT:", e);
}
"""
with open('test_run.js', 'w', encoding='utf-8') as f:
    f.write(js_mock)
