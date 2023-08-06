from mailhound.Modules.sitemap import site_map
from mailhound.Modules.Datasets import datasets
import asyncio
import argparse


async def Emails(domain: str, sitemap: str = None) -> set[str]:
    emails = set()

    if sitemap is not None:
        results = await asyncio.gather(site_map(file_path=sitemap, domain=domain), datasets(domain=domain))
        for result in results:
            emails.update(result)
    else:
        results = await datasets(domain)
        emails.update(results)

    return emails


async def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, metavar='domain', help='site.com')
    parser.add_argument('-s', '--sitemap', type=str, metavar='', default=None, help='BurpSuite sitemap')
    args = parser.parse_args()

    domain: str = args.domain
    sitemap: str = args.sitemap

    emails = await Emails(domain=domain, sitemap=sitemap)
    print('\n'.join(str(item) for item in emails))


def main():
    asyncio.run(run())
