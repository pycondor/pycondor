.. _changelog:

:github_url: https://github.com/jrbourbeau/pycondor

*************
Release Notes
*************

Version 0.1.5 (TBD)
-------------------

**New Features**:

* Added ``dagman_progress`` command line tool for displaying a progress bar for Dagman jobs. (See `PR #45 <https://github.com/jrbourbeau/pycondor/pull/45>`_)

**Bug Fixes**:

* Fixed bug where the queue parameter for a Job was not written to the job submit file when the Job was built by a Dagman. (See `PR #42 <https://github.com/jrbourbeau/pycondor/pull/42>`_)
* Fixed bug that caused a filename mismatch between a ``Job`` submit file and the error/log/output files when a named argument is added to a ``Job``, and the ``Job`` is built with ``fancyname=True``. (See `PR #45 <https://github.com/jrbourbeau/pycondor/pull/48>`_)


Version 0.1.4 (2017-06-08)
--------------------------

**Changes**:

* Fixes bug where Jobs that have no arguments, when submitted from a Dagman, were not included in the dag submit file. (See `issue #33 <https://github.com/jrbourbeau/pycondor/issues/33>`_)


Version 0.1.3 (2017-06-07)
--------------------------

**Changes**:

* Adds subdag support. Now Dagman objects can be added to other Dagman object with the new ``add_subdag`` class method.


Version 0.1.2 (2017-05-26)
--------------------------

**Changes**:

* Adds ``retry`` option to the Job ``add_arg`` method. This allows the user to specify the number of times to re-submit this node in the Job if the node fails.
* Adds ``name`` option to the Job ``add_arg`` method. If a name is specified, then a separate set of log, output, and error files will be generated specifically for that node.
* Adds ``tests`` directory in ``pycondor``!


Version 0.1.1 (2017-05-10)
--------------------------

**Changes**:

* Adds ``use_unique_id`` option when creating a Job object. This will then create a separate error, log, and output file for each of the arguments in the Job ``args`` list.
* Adds ``extra_lines`` option when creating a Dagman object (similar to the Job object).
* Replaces all occurances of ``os.system()`` with ``subprocess.Popen()``. This won't affect anything the user touches, just modernizing under-the-hood stuff.


Version 0.1.0 (2017-04-19)
--------------------------

**Changes**:

* Adds ``request_cpus`` attribute to Job object to make it easier to request a specified number of CPUs.
* Adds ``pycondor.get_queue()`` feature to get ``condor_q`` information.
* Job and Dagman object methods now return ``self``.
* Fixed typo in logger formatting.
