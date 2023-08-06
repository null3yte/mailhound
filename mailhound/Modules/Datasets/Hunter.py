import aiohttp
import re


async def hunter(domain: str, key: str) -> set[str]:
    """
    Retrieves email addresses associated with a given domain using the Hunter.io API.

    :param domain: The domain to search for email addresses.
    :param key: The API key for accessing the Hunter.io API.
    :return: A set of email addresses associated with the domain.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={key}") as response:
            res = await response.json()
            emails_list = re.findall(r"'value': '(.*?)'", str(res))
            return set(emails_list)
