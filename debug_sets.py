import asyncio
from playwright.async_api import async_playwright
import subprocess
import time

async def main():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8084'])
    time.sleep(2)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto('http://localhost:8084/index.html#/sets')
            await page.wait_for_timeout(3000)
            
            # Check sets
            cards = await page.query_selector_all('.bg-brand-surface') # Set cards have this class
            print(f"Found {len(cards)} set cards")
            
            await page.screenshot(path='/home/jules/verification/debug_sets.png', full_page=True)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server.terminate()

if __name__ == '__main__':
    asyncio.run(main())
