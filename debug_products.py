import asyncio
from playwright.async_api import async_playwright
import subprocess
import time
import os

async def main():
    # Start server
    server = subprocess.Popen(['python3', '-m', 'http.server', '8081'])
    time.sleep(2)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto('http://localhost:8081/index.html')
            # Wait for data to load
            await page.wait_for_timeout(3000)
            
            cards = await page.query_selector_all('.bg-white.rounded-2xl')
            print(f"Found {len(cards)} cards")
            
            for i, card in enumerate(cards[:5]):
                text = await card.inner_text()
                print(f"Card {i} text: {text[:50]}...")

            await page.screenshot(path='/home/jules/verification/debug_products_py.png', full_page=True)
            
            # Check if menu.json was loaded
            # Check network requests
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server.terminate()

if __name__ == '__main__':
    asyncio.run(main())
