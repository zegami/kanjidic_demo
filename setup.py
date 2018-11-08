#!/usr/bin/env python3
#
# Copyright 2017 Zegami Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Install script for Zegami KANJIDIC demo."""

import os

import setuptools


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
        return f.read()


setuptools.setup(
    name="Zegami KANJIDIC demo",
    version="0.3",
    description="Zegami demo using KANJIDIC",
    long_description=readme(),
    licence="Apache-2.0",
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
