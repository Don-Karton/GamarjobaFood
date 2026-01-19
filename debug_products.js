import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Start a local server in the background
  const { exec } = require('child_process');
  const server = exec('python3 -m http.server 8081');
  
  await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for server to start
  
  try {
    await page.goto('http://localhost:8081/index.html');
    await page.waitForTimeout(2000); // Wait for fetch
    
    const productCardsCount = await page.locator('.bg-white.rounded-2xl').count();
    console.log(`Found ${productCardsCount} product cards.`);
    
    const html = await page.content();
    if (html.includes('Loading...')) {
        console.log("Still loading...");
    }
    
    await page.screenshot({ path: '/home/jules/verification/debug_products.png', fullPage: true });
    
    // Check for errors in console
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
    server.kill();
  }
})();
