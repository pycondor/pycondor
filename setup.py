'''
James Bourbeau 2017
PyCondor
Author: James Bourbeau <jamesbourbeau.com>

License: MIT
Code repository: https://github.com/jrbourbeau/pycondor
'''

from setuptools import setup, find_packages
import pycondor

VERSION = pycondor.__version__

setup(
    name='PyCondor',
    version=VERSION,
    description='Python utility for HTCondor',
    url='https://github.com/jrbourbeau/pycondor',
    author='James Bourbeau',
    author_email='jbourbeau@wisc.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords='python condor htcondor high-throughput computing utility tool',
    packages=find_packages(),
    package_data={'': ['LICENSE',
                       'README.md'],
                  'examples': ['examples/savelist.py',
                  'examples/job_example.py',
                  'examples/job_arguments_example.py',
                  'examples/dagman_example.py',
                  'examples/jagman_parentchild_example.py']}
)
