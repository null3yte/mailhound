import asyncio
from mailhound.Modules.Datasets.Minelead import minelead
from mailhound.Modules.Datasets.Hunter import hunter
from mailhound.Modules.Datasets.Emailf import emailf
from mailhound.Modules.Datasets.Snov import snov
from mailhound.Modules.Datasets.Skymem import skymem
from mailhound.configs import *


async def datasets(domain: str) -> set[str]:
    """
    Retrieves email addresses associated with a given domain from multiple datasets and merges the results.

    :param domain: The domain to search for email addresses.
    :return: A set of email addresses associated with the domain.
    """

    link = {
        "hunter": hunter,
        "minelead": minelead,
        "emailf": emailf,
        "snov": snov,
        "skymem": skymem,
    }
    # Configuration for dataset providers' keys or credentials
    config = {
        "hunter": hunter_key,
        "minelead": minelead_key,
        "snov": snov_up,
    }

    tasks = []

    # Always run these functions
    for provider in ["emailf", "skymem"]:
        task = link.get(provider, None)
        if task is not None:
            tasks.append(asyncio.create_task(task(domain)))

    for provider, key in config.items():
        if key is not None:
            task = link.get(provider, None)
            if task is not None:
                tasks.append(asyncio.create_task(task(domain, key)))

    results = await asyncio.gather(*tasks)

    emails = set()
    for result in results:
        emails.update(result)

    emails.discard('')

    return emails


if __name__ == '__main__':
    asyncio.run(datasets('ford.com'))
