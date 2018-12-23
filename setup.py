from setuptools import find_packages
from setuptools import setup


setup(
    name="dumbpm",
    version="0.0.2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[],
    packages=find_packages(exclude=("tests*", "testing*")),
    entry_points={"console_scripts": ["dumbpm=dumbpm.cmd:main"]},
)
