import asyncio
from playwright.async_api import async_playwright
from mailhound.Modules import extract_emails


async def emailf(domain: str) -> set[str]:
    """
    Retrieves the email address format for a given domain from "email-format.com".

    :param domain: The domain to search for email addresses.
    :return: A set of email addresses extracted.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(f"https://www.email-format.com/d/{domain}/")
        page_content = await page.content()
        await browser.close()

        return await extract_emails(text=page_content, domain=domain)


if __name__ == '__main__':
    email_set = asyncio.run(emailf('disney.com'))
    emails = '\n'.join(email_set)
    print(emails)
