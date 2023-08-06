from mailhound.Modules import extract_emails


async def site_map(file_path: str, domain: str):
    with open(file_path, encoding='utf-8') as sm:
        return await extract_emails(text=sm.read(), domain=domain)
