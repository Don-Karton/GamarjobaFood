from playwright.sync_api import sync_playwright, expect
import time

def verify_ux_changes(page):
    # 1. Start on Home
    page.goto("http://localhost:5500/#/")
    time.sleep(1)

    # 2. Go to Sets list using the bottom nav link
    page.get_by_role("link", name="view_list Sets").click()
    time.sleep(1)
    page.screenshot(path="verification/sets_list.png")

    # 3. Click on first Set tune button
    # In SetCard: <Link to={`/set/${setDef.id}`} ...><span className="material-symbols-outlined ...">tune</span></Link>
    # There's also the card itself which might be a link?
    # Actually SetCard has one Link for the tune button.
    page.locator('a[href^="#/set/"]').first.click()
    time.sleep(1)

    # Verify SetEditor is open
    expect(page.get_by_role("button", name="Save Set")).to_be_visible()
    page.screenshot(path="verification/set_editor_top.png")

    # 4. Scroll down in SetEditor
    # The scrollable container has class "flex-1 overflow-y-auto hide-scrollbar"
    # We'll use the mouse wheel
    page.mouse.wheel(0, 500)
    time.sleep(2) # Give it time to scroll
    page.screenshot(path="verification/set_editor_scrolled.png")

    # 5. Click on a product in SetEditor
    # Products are linked via <Link to={`/product/${row.productId}`} ...>
    # Let's find one that is visible
    page.locator('a[href^="#/product/"]').first.click()
    time.sleep(1)

    # Verify ProductPage is open
    page.screenshot(path="verification/product_page_1.png")

    # 6. Navigate back
    page.go_back()
    time.sleep(1)

    # Verify we are back in SetEditor and scroll position is kept
    page.screenshot(path="verification/set_editor_restored.png")

    # 7. Test horizontal swipe on ProductPage
    # Go to a product again
    page.locator('a[href^="#/product/"]').first.click()
    time.sleep(1)

    # Simulate swipe left (Next)
    # Using mouse events to simulate touch
    page.mouse.move(300, 300)
    page.mouse.down()
    page.mouse.move(50, 300)
    page.mouse.up()
    time.sleep(1)
    page.screenshot(path="verification/product_swiped_next.png")

    # Simulate swipe right (Previous)
    page.mouse.move(50, 300)
    page.mouse.down()
    page.mouse.move(300, 300)
    page.mouse.up()
    time.sleep(1)
    page.screenshot(path="verification/product_swiped_prev.png")

    # Simulate swipe down (Close)
    # Move to top first to ensure we are at scrollTop 0
    # Actually just swiping down should work if we didn't scroll the product page
    page.mouse.move(200, 100)
    page.mouse.down()
    page.mouse.move(200, 400)
    page.mouse.up()
    time.sleep(1)
    page.screenshot(path="verification/product_closed_by_swipe.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a mobile-like viewport
        context = browser.new_context(
            viewport={"width": 375, "height": 667},
            has_touch=True
        )
        page = context.new_page()
        try:
            verify_ux_changes(page)
        finally:
            browser.close()
