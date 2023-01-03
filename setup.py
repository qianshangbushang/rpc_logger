#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :setup.py.py
# @Time      :2022/12/29 15:12


import setuptools

setuptools.setup(
    name='rpclogger',
    version='0.1.0',
    description='report log to remote server',
    author='houjinjing',
    author_email='',
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=['rpclogger'],
    install_requires=["requests", "yaml", "loguru"]
)
