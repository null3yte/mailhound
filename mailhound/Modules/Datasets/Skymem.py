from mailhound.Modules import extract_emails
import asyncio
import aiohttp
import re


async def fetch(session, url: str):
    """
    Fetches the content of a given URL using an aiohttp session.

    :param session: The aiohttp session.
    :param url: The URL to fetch.
    :return: The text content of the response.
    """
    async with session.get(url) as response:
        return await response.text()


async def get_emails(domain: str, enc_domain: str, page: int) -> set[str]:
    """
    Retrieves email addresses from a specific page of a domain on Skymem.

    :param domain: The domain to search for email addresses.
    :param enc_domain: The encoded domain used in the Skymem URL.
    :param page: The page number to retrieve emails from.
    :return: A set of email addresses on the specified page.
    """
    addr = 'https://www.skymem.info'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=addr + f'/domain/{enc_domain}?p={page}') as response:
            html = await response.text()
            emails = await extract_emails(text=html, domain=domain)
            return emails


async def skymem(domain: str) -> set[str]:
    """
    Retrieves email addresses associated with a given domain from Skymem.

    :param domain: The domain to search for email addresses.
    :return: A set of email addresses associated with the domain.
    """
    emails = set()
    addr = 'https://www.skymem.info'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=addr + f'/srch?q={domain}&ss=home') as response:
            html = await response.text()
            enc_domain = re.findall(r"Doc\.DomainEmails\.IdEntity='(.*?)'", html)[0]
            if enc_domain:
                tasks = [asyncio.ensure_future(get_emails(domain, enc_domain, page)) for page in range(1, 11)]
                results = await asyncio.gather(*tasks)
                for page_emails in results:
                    if page_emails:
                        emails.update(page_emails)

    return emails


if __name__ == '__main__':
    email_set = asyncio.run(skymem('disney.com'))
    emails = '\n'.join(email_set)
    print(emails)
