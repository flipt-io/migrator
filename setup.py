from setuptools import setup, find_packages

setup(
    name="flipt-migrate",
    version="0.1.0",
    author="Flipt Devs",
    author_email="dev@flipt.io",
    description="A CLI tool to migrate feature flags from one source (e.g. competitor) to Flipt",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "flipt-migrate=flipt_migrate.cli:main",
        ],
    },
)
