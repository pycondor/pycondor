.. PyCondor documentation master file, created by
   sphinx-quickstart on Wed Jun 14 16:49:05 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:github_url: https://github.com/pycondor/pycondor

********
PyCondor
********

.. image:: https://travis-ci.org/pycondor/pycondor.svg?branch=master
    :target: https://travis-ci.org/pycondor/pycondor

.. image:: https://codecov.io/gh/pycondor/pycondor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pycondor/pycondor

.. image:: https://img.shields.io/pypi/v/pycondor.svg
    :target: https://pypi.org/project/PyCondor/

.. image:: https://img.shields.io/pypi/l/pycondor.svg
    :target: https://pypi.org/project/PyCondor/

.. image:: https://img.shields.io/pypi/pyversions/pycondor.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/PyCondor/

**PyCondor (Python HTCondor) is a tool to help build and submit workflows to HTCondor in a straight-forward manner with minimal hassle.**

With just a few lines of code, you can get PyCondor up and running:

.. code-block:: python

    from pycondor import Job
    job = Job(name='examplejob', executable='my_script.py')
    job.build_submit()


.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   overview
   installation
   tutorial

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   api
   cli
   visualize
   examples
   changelog
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Useful links

   PyCondor @ GitHub <https://github.com/pycondor/pycondor>
   PyCondor @ PyPI <https://pypi.org/project/PyCondor/>
   Issue tracker <https://github.com/pycondor/pycondor/issues>


Questions & Bug Reports
-----------------------

PyCondor is an open-source project and contributions are always welcome from
anyone. If you have a question, would like to propose a new feature, or submit
a bug report, feel free to open up an issue on our `issue tracker on GitHub <https://github.com/pycondor/pycondor/issues>`_.
