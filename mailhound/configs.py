import yaml
import os

providers = os.path.expanduser('~/.config/mailhound/providers.yaml')
with open(providers, 'r') as f:
    data = yaml.safe_load(f)

for key, value in data.items():
    if value == 'null':
        data[key] = None

minelead_key = data.get('minelead_key')
hunter_key = data.get('hunter_key')
snov_up = data.get('snov_up')
