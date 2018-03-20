#!/usr/bin/env python

DISTNAME = 'PyCondor'
DESCRIPTION = 'Python utility for HTCondor'
MAINTAINER = 'James Bourbeau'
MAINTAINER_EMAIL = 'james@jamesbourbeau.com'
URL = 'https://github.com/jrbourbeau/pycondor'
LICENSE = 'MIT'
LONG_DESCRIPTION = '''Python utility for HTCondor

Helps construct submit files for submitting jobs and dagmans to HTCondor

Please refer to the online documentation at
https://jrbourbeau.github.io/pycondor/
'''

from setuptools import setup, find_packages
import pycondor

VERSION = pycondor.__version__

with open('requirements/default.txt') as fid:
    INSTALL_REQUIRES = [l.strip() for l in fid.readlines() if l]

setup(
    name=DISTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=MAINTAINER,
    author_email=MAINTAINER_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    keywords='python condor htcondor high-throughput computing utility tool',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points = {
        'console_scripts': ['dagman_progress=pycondor.cli:dagman_progress',
                            'pycondor=pycondor.cli:cli',
                            ],
    },
    package_data={'': ['LICENSE',
                       'README.md'],
                  'examples': ['examples/savelist.py',
                               'examples/job_example.py',
                               'examples/job_arguments_example.py',
                               'examples/dagman_example.py',
                               'examples/dagman_parentchild_example.py',
                               'examples/subdag_example.py']}
)
