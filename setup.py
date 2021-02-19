#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MediaCurator",
    version="0.0.5",
    author="Fabrice Quenneville",
    author_email="fab@fabq.ca",
    url="https://github.com/fabquenneville/MediaCurator",
    download_url="https://pypi.python.org/pypi/MediaCurator",
    project_urls={
        "Bug Tracker": "https://github.com/fabquenneville/MediaCurator/issues",
        "Documentation": "https://fabquenneville.github.io/MediaCurator/",
        "Source Code": "https://github.com/fabquenneville/MediaCurator",
    },
    description="MediaCurator is a Python command line tool to manage a media database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Multimedia :: Video :: Conversion",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points = {
        'console_scripts': ['mediacurator=mediacurator.mediacurator:main'],
    },
    keywords=[
        "codecs", "filters", "video", "x265", "av1", "media-database", "python-command", "hevc"
    ],
    install_requires=[
        "pathlib","colorama"
    ],
    license='GPL-3.0',
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=True,
)