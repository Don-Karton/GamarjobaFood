import asyncio
from playwright.async_api import async_playwright
import subprocess
import time

async def main():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8082'])
    time.sleep(2)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"PAGE LOG: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err.message}"))
        
        try:
            await page.goto('http://localhost:8082/index.html')
            await page.wait_for_timeout(5000) # Give it more time
            
            # Check products
            cards = await page.query_selector_all('article') # Products are articles
            print(f"Found {len(cards)} product articles")
            
            await page.screenshot(path='/home/jules/verification/debug_products_v2.png', full_page=True)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server.terminate()

if __name__ == '__main__':
    asyncio.run(main())
