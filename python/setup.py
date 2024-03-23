import setuptools
from distutils.core import setup


setup(
    name='plaintext-daw',
    version='0.0.0',
    description='Plaintext DAW',
    author='Steve Grice',
    author_email='steve@pagekeytech.com',
    packages=['plaintext_daw'],
    entry_points={
        'console_scripts': ['plaintext-daw=plaintext_daw.cli:cli_entry_point'],
    },
    install_requires=[
        'numpy',
        'pyyaml',
        'PyQt5',
        "pydub",
    ],
)
