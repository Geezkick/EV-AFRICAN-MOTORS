from setuptools import setup, find_packages

setup(
    name="ev_african_motors",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'click',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'ev-african-motors=lib.cli.cli:main',
        ],
    },
)