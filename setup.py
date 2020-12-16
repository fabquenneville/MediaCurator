#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mediacurator",
    version="0.0.1",
    author="Fabrice Quenneville",
    author_email="fab@fabq.ca",
    url="https://github.com/fabquenneville/MediaCurator",
    description="MediaCurator is a Python command line tool to manage a media database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="TBD",
    packages=setuptools.find_packages(exclude=("mediacurator.library",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "codecs", "filters", "video", "x265", "av1", "media-database", "python-command", "hevc"
    ],
    install_requires=[
        "pathlib","colorama"
    ],
    license='GPL-3.0',
    python_requires='>=3.6',
)