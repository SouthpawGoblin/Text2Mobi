#!/usr/bin/env python

from setuptools import setup

setup(
    name="text2mobi",
    version="0.1.0",
    author="Roger-Qi",
    author_email="goblin-qyz@163.com",
    description="Convert text string or .txt/.html file to .mobi file for Amazon Kindle",
    packages=["text2mobi"],
    install_requires=["pyquery>=1.2.17"],
    include_package_data=True,
    url="https://github.com/SouthpawGoblin/Text2Mobi",
    keywords="text,kindle,ebook,mobi,convert"
)
