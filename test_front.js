const puppeteer = require('puppeteer');
(async () => {
    try {
        const browser = await puppeteer.launch({headless: true});
        const page = await browser.newPage();
        
        let errors = [];
        page.on('pageerror', error => {
            errors.push(error.message);
        });
        
        await page.goto('http://127.0.0.1:8080');
        await page.waitForTimeout(1000);
        
        console.log("ERRORS:", errors.length);
        if (errors.length > 0) {
            console.log(errors);
        }
        await browser.close();
    } catch(e) {
        console.log("Puppeteer not installed or failed", e.message);
    }
})();
