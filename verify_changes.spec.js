const { test, expect } = require('@playwright/test');
const path = require('path');

test('Verify images and scroll reset on category switch', async ({ page }) => {
  // Start server
  const { exec } = require('child_process');
  const server = exec('npx http-server -p 5500');
  await new Promise(r => setTimeout(r, 2000));

  try {
    await page.goto('http://localhost:5500');
    await page.waitForLoadState('networkidle');

    // 1. Verify images are present
    const images = await page.locator('div[style*="background-image"]').all();
    console.log(`Found ${images.length} elements with background-image`);
    expect(images.length).toBeGreaterThan(0);

    // 2. Verify scroll reset
    // Find the scrollable main element
    const main = page.locator('main');

    // Scroll down
    await main.evaluate(node => node.scrollTop = 500);
    let scrollTopBefore = await main.evaluate(node => node.scrollTop);
    console.log(`Scroll top before switch: ${scrollTopBefore}`);
    expect(scrollTopBefore).toBeGreaterThan(0);

    // Switch category (aside sidebar buttons)
    const pastryButton = page.locator('aside button').filter({ hasText: /PASTRY|Выпечка|ცომეული/i });
    await pastryButton.click();
    await page.waitForTimeout(500); // Wait for potential smooth scroll or re-render

    let scrollTopAfter = await main.evaluate(node => node.scrollTop);
    console.log(`Scroll top after switch: ${scrollTopAfter}`);
    expect(scrollTopAfter).toBe(0);

    // Screenshot
    await page.screenshot({ path: 'verification/category_switch.png' });

  } finally {
    server.kill();
  }
});
