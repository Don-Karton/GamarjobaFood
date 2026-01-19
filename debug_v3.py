import asyncio
from playwright.async_api import async_playwright
import subprocess
import time

async def main():
    server = subprocess.Popen(['python3', '-m', 'http.server', '8085'])
    time.sleep(2)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto('http://localhost:8085/index.html')
            await page.wait_for_timeout(5000)
            
            # Check for cards (using a more general selector or just taking screenshot)
            await page.screenshot(path='/home/jules/verification/debug_products_v3.png', full_page=True)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server.terminate()

if __name__ == '__main__':
    asyncio.run(main())
