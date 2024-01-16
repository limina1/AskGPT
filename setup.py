# Path /setup.py

from setuptools import setup, find_packages

setup(
    name='askgpt',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'askgpt = askgpt.__main__:main'
        ]
    },
    )
