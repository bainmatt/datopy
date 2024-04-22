from setuptools import setup

if __name__ == "__main__":
    setup()


# from setuptools import setup, find_packages


# def read(fname: str):
#     with open(fname) as file:
#         return file.read()


# setup(
#     name='datopy',
#     version='0.1',
#     author="Matthew Bain",
#     description = ("Assorted examples and tools for data modeling, ETL,"
#                    "and web scraping."),
#     url = "https://github.com/bainmatt/data-tools",
#     license='MIT',
#     # packages=find_packages(exclude=(
#     #     'datopy/tests', 'datopy/data', 'datopy/_examples', 'datopy/_settings', 'datopy/_media_scrape')),
#     packages=find_packages(),
#     include_package_data=False,
#     long_description=read("README.md"),
#     install_requires=[
#         "requests",
#         "pandas",
#         "pydantic",
#         "jsonschema",
#         "python-dotenv",
#         "bs4",
#         # "openssl",
#         # "pycurl",
#         "wptools",
#         "cinemagoer",
#         "spotipy",
#     ],
#     classifiers=[
#         'Development Status :: 4 - Beta',
#         'Topic :: Data Management',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python :: 3.10',
#     ],
# )
