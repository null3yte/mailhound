import aiohttp
import re


async def minelead(domain: str, key: str) -> set[str]:
    """
    Retrieves email addresses associated with a given domain using the Minelead API.

    :param domain: The domain to search for email addresses.
    :param key: The API key for accessing the Minelead API.
    :return: A set of email addresses associated with the domain.
    """
    emails = set()

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.minelead.io/v1/search/?domain={domain}&key={key}") as response:
            if response.status == 200:
                hres = await response.text()  # HTTP response
                emails_nf = re.findall(r"\"email\": \"(.*?)\",", hres)
                emails = {re.sub(rf"(.*?)\*(.*?)@{domain}", '', email) for email in emails_nf if email}

    return emails
