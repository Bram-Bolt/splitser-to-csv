from setuptools import setup, find_packages

setup(
    name="splitser-to-csv",
    version="0.1.0",
    description="Convert splitser PDF to CSV",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bram Bolt",
    author_email="contact@brambolt.me",
    url="https://github.com/bram-bolt/splitser-to-csv",
    packages=find_packages(),
    install_requires=[
        "pypdf",
    ],
    entry_points={
        "console_scripts": [
            "app=app.main:main",
        ],
    },
)
