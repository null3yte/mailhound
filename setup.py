from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import subprocess
import mailhound
import yaml


class PostInstallCommand(install):
    def run(self):
        subprocess.check_call(['playwright', 'install'])
        install.run(self)


providers_file = Path('~/.config/mailhound/providers.yaml').expanduser()
providers_file.parent.mkdir(parents=True, exist_ok=True)

new_providers = {
    'snov_up': None,
    'minelead_key': None,
    'hunter_key': None,
}

# If the providers.yaml file exists, load its content and update the new_providers dictionary
if providers_file.is_file():
    with providers_file.open('r') as f:
        providers = yaml.safe_load(f)
        for key in new_providers.keys():
            if key in providers:
                new_providers[key] = providers[key]

with providers_file.open('w') as f:
    yaml.dump(new_providers, f)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mailhound',
    version=mailhound.__version__,
    author='null3yte',
    description='A simple tool to find emails of a domain',
    include_package_data=True,
    license='MIT',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/null3yte/mailhound",
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mailhound=mailhound.__main__:main',
        ],
    },
    install_requires=[
        "aiohttp~=3.8.4",
        "PyYAML~=6.0.1",
        "playwright~=1.36.0",
        "setuptools~=65.5.0",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'install': PostInstallCommand,
    }
)
