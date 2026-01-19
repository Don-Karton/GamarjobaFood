import asyncio
from playwright.async_api import async_playwright
import subprocess
import time

async def main():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8083'])
    time.sleep(2)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto('http://localhost:8083/index.html')
            await page.wait_for_timeout(3000)
            
            # Click "Appetizers & Bruschettas" (2nd item in sidebar)
            sidebar_items = await page.query_selector_all('.sidebar-item')
            print(f"Found {len(sidebar_items)} sidebar items")
            if len(sidebar_items) > 1:
                await sidebar_items[1].click()
                await page.wait_for_timeout(1000)
                cards = await page.query_selector_all('article')
                print(f"Found {len(cards)} cards in category 1")
                
                # Check text of first card
                if len(cards) > 0:
                    text = await cards[0].inner_text()
                    print(f"First card text: {text[:50]}")

            await page.screenshot(path='/home/jules/verification/debug_category_click.png', full_page=True)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server.terminate()

if __name__ == '__main__':
    asyncio.run(main())
