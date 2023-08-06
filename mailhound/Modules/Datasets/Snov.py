from playwright.async_api import async_playwright
from mailhound.Modules import extract_emails

login_url = 'https://app.snov.io/login'


async def snov(domain: str, key: str):
    """
    Retrieves email addresses associated with a given domain using the Snov.io platform.

    :param domain: The domain to search for email addresses.
    :param key: The Snov.io login credentials in the format 'username:password'.
    :return: A set of email addresses associated with the domain.
    """
    split_string = key.split(":")
    username = split_string[0]
    password = split_string[1]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(login_url)

        # Fill out the login form
        await page.fill('input[data-test="email"]', username)
        await page.fill('input[data-test="password"]', password)
        await page.click('button[data-test="submit-form"]')

        await page.wait_for_load_state('networkidle')
        await page.goto(f'https://app.snov.io/domain-search?name={domain}&tab=emails')
        await page.wait_for_load_state('networkidle')

        html = await page.content()
        await browser.close()

        return await extract_emails(html, domain)
