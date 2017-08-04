from setuptools import setup, find_packages

setup(
    name = "dns-domain-expiration-checker",
    version = "6.0",
    author = "Matty",
    author_email = "matty91@gmail.com",
    url = 'https://github.com/Matty9191/dns-domain-expiration-checker',
    description = "DNS DOmain Expiration Checker",
    keywords = "DNS Domain Expiration Bind",
    packages = find_packages(),
    install_requires = ['python-dateutil'],
)
