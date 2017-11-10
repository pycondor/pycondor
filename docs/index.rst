.. PyCondor documentation master file, created by
   sphinx-quickstart on Wed Jun 14 16:49:05 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:github_url: https://github.com/jrbourbeau/pycondor

.. toctree::
   :maxdepth: 3
   :caption: User Guide
   :hidden:

   api
   examples
   monitoring
   changelog
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Useful links
   :hidden:

   PyCondor @ GitHub <https://github.com/jrbourbeau/pycondor>
   PyCondor @ PyPI <https://pypi.python.org/pypi/PyCondor>
   Issue tracker <https://github.com/jrbourbeau/pycondor/issues>



**********************
PyCondor Documentation
**********************

.. image:: https://travis-ci.org/jrbourbeau/pycondor.svg?branch=master
    :target: https://travis-ci.org/jrbourbeau/pycondor

.. image:: https://codecov.io/gh/jrbourbeau/pycondor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jrbourbeau/pycondor

.. image:: https://img.shields.io/pypi/v/pycondor.svg
    :target: https://pypi.python.org/pypi/PyCondor/

.. image:: https://img.shields.io/pypi/l/pycondor.svg
    :target: https://pypi.python.org/pypi/PyCondor/

`PyCondor
<https://github.com/jrbourbeau/pycondor/>`_ (Python HTCondor) is a tool that helps build and submit HTCondor jobs in a straight-forward manner with minimal hassle.

With just a couple lines of code, you can get PyCondor up and running!

.. code-block:: python

    >>> import pycondor
    >>> job = pycondor.Job('examplejob', '/path/to/my_script.py')
    >>> job.build_submit()


==========
Motivation
==========
`HTCondor <https://research.cs.wisc.edu/htcondor/>`_ is a an open-source workload management system for high-throughput computing tasks developed at the University of Wisconsin–Madison. It is an incredibly useful and versatile tool. However, the process of submitting jobs to HTCondor, especially when there are inter-job dependencies, can quickly become both tedious and complex. PyCondor is a tool to help streamline this job submission process through a user-friendly API and built-in functionality to automate common tasks.

============
Installation
============


For the current release version of PyCondor

.. code-block:: shell

    $ pip install pycondor

For the latest development version, ``pip`` install directly from GitHub

.. code-block:: shell

    $ pip install git+https://github.com/jrbourbeau/pycondor.git


==========
User Guide
==========

* :doc:`api`
* :doc:`examples`
* :doc:`monitoring`
* :doc:`changelog`
* :doc:`contributing`
