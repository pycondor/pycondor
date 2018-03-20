#!/usr/bin/env python

import os
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command

NAME = 'PyCondor'
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

here = os.path.abspath(os.path.dirname(__file__))

# Want to read in package version number from __version__.py
about = {}
with open(os.path.join(here, 'pycondor', '__version__.py'), 'r') as f:
    exec(f.read(), about)
    VERSION = about['__version__']

with open('requirements/default.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


class UploadCommand(Command):
    """Support setup.py upload"""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='python condor htcondor high-throughput computing utility tool',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
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
                               'examples/subdag_example.py']},
    cmdclass={
        'upload': UploadCommand,
    },
)
