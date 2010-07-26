from setuptools import setup, find_packages

setup(
    name = "PyLINQ",
    version = "0.1",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    include_package_data = True,

    # metadata for upload to PyPI
    author = "Insophia",
    author_email = "olveyra@insophia.com, andres@insophia.com",
    description = "PyLINQ it's a pure python port of the Microsoft LINQ project",
    license = "GPL v2",
    keywords = "pylinq linq collections iterators generators query language",
    url = "http://github.com/kalessin/PyLINQ",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
