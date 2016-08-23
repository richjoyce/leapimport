#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='leapimport',
    version='0.1.1',
    description="Simple package to import binary LeapMotion recording data.",
    long_description=readme + '\n\n' + history,
    author="Richard Joyce",
    author_email='rjoyce@ucdavis.edu',
    url='https://github.com/richjoyce/leapimport',
    packages=[
        'leapimport',
    ],
    package_dir={'leapimport':
                 'leapimport'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='leapimport',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
