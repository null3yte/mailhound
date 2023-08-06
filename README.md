# Installation
```bash
git clone https://github.com/null3yte/mailhound.git
cd mailhound
pip install .
```
# Configuration

After installation, Mailhound can function without requiring API keys, but configuring API keys is necessary for better
results.

- [minelead](https://minelead.io/)
- [hunter](https://hunter.io/)
- [snov](https://snov.io/)

```yaml
# $HOME/.config/mailhound/providers.yaml
minelead_key: 'API_KEY'
hunter_key: 'API_KEY'
snov_up: 'username:password'
```

# Usage

```bash
mailhound -h
```

```text             
usage: mailhound [-h] [-s] domain

positional arguments:
  domain           site.com

options:
  -h, --help       show this help message and exit
  -s , --sitemap   BurpSuite sitemap
```
