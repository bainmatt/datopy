from setuptools import setup, find_packages

def read(fname: str):
    with open(fname) as file:
        return file.read()
    

setup(
    name='datatoolz',
    version='0.1',
    author="Matthew Bain",
    description = ("Assorted examples and tools for data modeling, ETL,"
                   "and web scraping."),
    url = "https://github.com/bainmatt/data-tools",
    license='MIT',
    packages=find_packages(exclude=(
        'datatools/tests', 'datatools/data', 'datatools/_examples', 'datatools/_settings', 'datatools/_media_scrape')),
    include_package_data=True,
    long_description=read("README.md"),
    install_requires=[
        "requests",
        "pandas",
        "pydantic",
        "jsonschema",
        "python-dotenv",
        "bs4",
        # "openssl",
        # "pycurl",
        "wptools",
        "cinemagoer",
        "spotipy",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Data Management',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
