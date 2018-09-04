#!/usr/bin/env python3
#
# Copyright 2017 Zegami Ltd

"""Install script for Zegami KANJIDIC demo."""

import os

import setuptools


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
        return f.read()


setuptools.setup(
    name="Zegami KANJIDIC demo",
    version="0.2",
    description="Zegami demo using KANJIDIC",
    long_description=readme(),
    url="https://zegami.com",
    author="Martin Packman",
    author_email="martin@zegami.com",
    packages=["zegami_kanjidic"],
    scripts=["ktoz"],
    install_requires=[
        "freetype-py >= 1",
        "Pillow >= 4",
        "requests >= 2.18",
    ],
)
