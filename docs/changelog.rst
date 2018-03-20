.. _changelog:

:github_url: https://github.com/jrbourbeau/pycondor

*************
Release Notes
*************

Version 0.3.0 (2018-03-20)
--------------------------

**New Features**:

* Added ``dag`` parameter to ``Job`` and ``Dagman`` object initializations. (See `PR #67 <https://github.com/jrbourbeau/pycondor/pull/67>`_)
* Added ``submit_options`` parameter to ``Job.submit_job`` and ``Dagman.submit_dag`` methods. ``kwargs`` and ``maxjobs`` parameters for these methods are deprecated in favor of ``submit_options``. (See `PR #71 <https://github.com/jrbourbeau/pycondor/pull/71>`_)
* Adds ``pycondor submit`` command. Also adds replaces ``dagman_progress`` command with ``pycondor monitor``. (See `PR #73 <https://github.com/jrbourbeau/pycondor/pull/73>`_)

**Changes**:

* Added a check for illegal characters in Dagman submit file node names when running HTCondor version 8.7.2 or newer. (See `PR #66 <https://github.com/jrbourbeau/pycondor/pull/66>`_)


**Bug Fixes**:

* Fixed bug so that ``BaseNode`` objects set their submit attribute to the current working directory if not provided directly or set via an environment variable. (See `PR #75 <https://github.com/jrbourbeau/pycondor/pull/75>`_)


Version 0.2.0 (2017-11-22)
--------------------------

**New Features**:

* Added ``dagman_progress`` command line tool for displaying a progress bar for Dagman jobs. (See `PR #45 <https://github.com/jrbourbeau/pycondor/pull/45>`_ and `PR #52 <https://github.com/jrbourbeau/pycondor/pull/52>`_)
* Added environment variable option for setting submit, error, log, and output directories. (See `PR #50 <https://github.com/jrbourbeau/pycondor/pull/50>`_)

**Bug Fixes**:

* Fixed bug where the queue parameter for a Job was not written to the job submit file when the Job was built by a Dagman. (See `PR #42 <https://github.com/jrbourbeau/pycondor/pull/42>`_)
* Fixed bug that caused a filename mismatch between a ``Job`` submit file and the error/log/output files when a named argument is added to a Job, and the Job is built with ``fancyname=True``. (See `PR #48 <https://github.com/jrbourbeau/pycondor/pull/48>`_)
* Fixed the Dagman submit file build procedure to include the name of Job named arguments in the Dagman node name (See `PR #53 <https://github.com/jrbourbeau/pycondor/pull/53>`_)


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
