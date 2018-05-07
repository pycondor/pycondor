.. PyCondor documentation master file, created by
   sphinx-quickstart on Wed Jun 14 16:49:05 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:github_url: https://github.com/jrbourbeau/pycondor

.. toctree::
   :maxdepth: 3
   :caption: User Guide
   :hidden:

   installation
   tutorial
   api
   cli
   examples
   changelog
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Useful links
   :hidden:

   PyCondor @ GitHub <https://github.com/jrbourbeau/pycondor>
   PyCondor @ PyPI <https://pypi.org/project/PyCondor/>
   Issue tracker <https://github.com/jrbourbeau/pycondor/issues>



********
PyCondor
********

.. image:: https://travis-ci.org/jrbourbeau/pycondor.svg?branch=master
    :target: https://travis-ci.org/jrbourbeau/pycondor

.. image:: https://codecov.io/gh/jrbourbeau/pycondor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jrbourbeau/pycondor

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


==========
Motivation
==========

`HTCondor <https://research.cs.wisc.edu/htcondor/>`_ is a an open-source workload management system for high-throughput computing tasks. It's an incredibly useful and versatile tool. However, the process of submitting jobs to HTCondor, especially in complex worflows where there are inter-job dependencies, can quickly become both tedious and intricate. PyCondor helps streamline the job submission process by providing

- A simple, user-friendly API
- Built-in functionality to automate common tasks
- Familiar terminology


========
Overview
========

The primary functionality of PyCondor is implemented in the **Job** and **Dagman** objects.

Job objects represent an executable (e.g. a shell command, Python script, etc.) that you would like to run on an HTCondor cluster. While Dagman (short for directed acyclic graph manager) objects are a collection of Jobs to be run. In addition to acting as a collection of Jobs, Dagman objects also allow you to

- Specify dependencies between Jobs (e.g. parent / child relationships)
- Retry failed Jobs
- Throttle the number of running Jobs
- Etc.

These features, in particular specifying inter-job dependencies, allow for the construction of complex workflows.


==========
User Guide
==========

* :doc:`installation`
* :doc:`tutorial`
* :doc:`api`
* :doc:`cli`
* :doc:`examples`
* :doc:`changelog`
* :doc:`contributing`
