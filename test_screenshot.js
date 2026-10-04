const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
        const page = await browser.newPage();
        await page.setViewport({width: 1280, height: 720});
        await page.goto('http://127.0.0.1:8080');
        await page.waitForTimeout(2000);
        await page.screenshot({path: 'screenshot.png'});
        await browser.close();
        console.log("Screenshot taken");
    } catch(e) {
        console.log("Puppeteer error:", e);
    }
})();
