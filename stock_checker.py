from playwright.sync_api import sync_playwright
from logger import setup_logger
logger = setup_logger()


def is_size_in_stock(url, size):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page.goto(url, timeout=60000)
        page.wait_for_selector("div.fr-chip-wrapper-er", timeout=15000)

        size_wrapper = page.locator(
            f"div.fr-chip-wrapper-er[data-test='{size}']"
        )

        if size_wrapper.count() == 0:
            browser.close()
            return False

        strike_icon = size_wrapper.locator(".chip-strikethrough-icon")
        in_stock = strike_icon.count() == 0

        browser.close()
        return in_stock


def get_all_sizes_stock(url, sizes):
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page.goto(url, timeout=60000)
        page.wait_for_selector("div.fr-chip-wrapper-er", timeout=15000)

        for size in sizes:
            size_wrapper = page.locator(
                f"div.fr-chip-wrapper-er[data-test='{size}']"
            )

            if size_wrapper.count() == 0:
                logger.warning(
                    f"Size {size} not found on page | treating as OUT_OF_STOCK"
                )
                results[size] = False
                continue


            strike_icon = size_wrapper.locator(".chip-strikethrough-icon")
            count = strike_icon.count()

            logger.debug(
                f"Size {size} | strike_icon_count={count} | "
                f"{'IN_STOCK' if count == 0 else 'OUT_OF_STOCK'}"
            )


            results[size] = (count == 0)

        browser.close()

    return results
