const { chromium } = require('playwright');

(async () => {

    const browser = await chromium.launch();

    const page = await browser.newPage();

    await page.goto(
        'file:///C:/ruta/index.html'
    );

    await page.pdf({
        path: 'cv.pdf',
        format: 'Letter',
        printBackground: true
    });

    await browser.close();

})();