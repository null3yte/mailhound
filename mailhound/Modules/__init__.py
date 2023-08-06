import re


async def extract_emails(text: str, domain: str) -> set[str]:
    reg_emails = re.compile(r'[a-zA-Z0-9.\-_]+@' + re.escape(domain.replace('www.', '')))
    emails = set(match.group().lower().strip() for match in reg_emails.finditer(text))
    return {email.replace('mailto:', '') for email in emails if len(email) > 1}
