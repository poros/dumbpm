from os import path

from setuptools import find_packages
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="dumbpm",
    version="0.2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["pandas"],
    packages=find_packages(exclude=("tests*", "testing*")),
    entry_points={"console_scripts": ["dumbpm=dumbpm.cmd:main"]},
    description="A pretty dumb PM.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
