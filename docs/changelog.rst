.. _changelog:

:github_url: https://github.com/pycondor/pycondor

*************
Release Notes
*************

Version 0.6.0 (TBD)
-------------------

**New Features**:

-

**Changes**:

-

**Bug Fixes**:

-

**Documentation**:

-


Version 0.5.0 (2018-11-05)
--------------------------

**New Features**:

- Adds ``visualize`` function and ``Dagman.visualize`` method for graph
  visualization. (See :pr:`122`)

**Changes**:

- Updates default values of the ``universe``, ``getenv``, and
  ``notification`` parameters for ``Job`` objects to ``None``. Now, unless
  explicitly given, the system defaults will be used.
  (See :pr:`115`)

**Bug Fixes**:

- Switch to using ``os.sep`` instead of ``'/'`` as a path separator.
  (See :pr:`107`)
- Fixed Windows-compability bug in ``Job.submit_job`` and ``Dagman.submit_dag``.
  (See :pr:`110`)
- Removes outdated reference to ``dagman_progress`` in ``entry_points`` of
  ``setup.py``. (See :pr:`113`)
- Resolves a ``ResourceWarning`` and ``DeprecationWarning`` raised while
  running the tests. (See :pr:`116`)
- Properly handles bytes arrays in ``get_condor_version``. (See :pr:`119`)
- Fixed a string formatting bug in ``Dagman.submit_dag`` and ``Job.submit_job``. (See :pr:`120`)

**Documentation**:

- Added conda installation instructions.
  (See :pr:`104`)
- Added API documentation for command line interface.
  (See :pr:`121`)


Version 0.4.0 (2018-06-07)
--------------------------

**New Features**:

- Adds the option to initialize a ``Job`` with an ``arguments`` parameter.
  (See :pr:`90` and :pr:`102`)
- Adds the option to initialize a ``Job`` with a ``retry`` parameter, which
  sets the default number of retries for all arguments of the Job if given.
  (See :pr:`90`)

**Changes**:

- Adds ``FutureWarning`` about changing the default values of the ``universe``, ``getenv``, and ``notification`` parameters for ``Job`` objects to None. (See :pr:`98`)
- Removes check that a ``Job`` executable path must exist locally when the ``Job`` is being built.
  (See :pr:`96`)
- Adds informative error message when ``Job.submit_job`` is called on a machine where the ``condor_submit`` command isn't available. (See :pr:`83`)
- Removes deprecated ``maxjobs`` and ``kwargs`` parameters for the ``Job.submit_job``, ``Job.build_submit``, ``Dagman.submit_dag``, and ``Dagman.build_submit`` methods. Also removes the deprecated ``dagman_progress`` command. (See :pr:`84`)


**Bug Fixes**:

- Fixes typo in ``pycondor monitor`` that was still referencing the old ``dagman_progress`` command. (See :pr:`81`)


Version 0.3.0 (2018-03-20)
--------------------------

**New Features**:

* Added ``dag`` parameter to ``Job`` and ``Dagman`` object initializations. (See :pr:`67`)
* Added ``submit_options`` parameter to ``Job.submit_job`` and ``Dagman.submit_dag`` methods. ``kwargs`` and ``maxjobs`` parameters for these methods are deprecated in favor of ``submit_options``. (See :pr:`71`)
* Adds ``pycondor submit`` command. Also adds replaces ``dagman_progress`` command with ``pycondor monitor``. (See :pr:`73`)

**Changes**:

* Added a check for illegal characters in Dagman submit file node names when running HTCondor version 8.7.2 or newer. (See :pr:`66`)


**Bug Fixes**:

* Fixed bug so that ``BaseNode`` objects set their submit attribute to the current working directory if not provided directly or set via an environment variable. (See :pr:`75`)


Version 0.2.0 (2017-11-22)
--------------------------

**New Features**:

* Added ``dagman_progress`` command line tool for displaying a progress bar for Dagman jobs.
  (See :pr:`45` and :pr:`52`)
* Added environment variable option for setting submit, error, log, and output directories.
  (See :pr:`50`)

**Bug Fixes**:

* Fixed bug where the queue parameter for a Job was not written to the job submit file when the Job was built by a Dagman. (See :pr:`42`)
* Fixed bug that caused a filename mismatch between a ``Job`` submit file and the error/log/output files when a named argument is added to a Job, and the Job is built with ``fancyname=True``. (See :pr:`48`)
* Fixed the Dagman submit file build procedure to include the name of Job named arguments in the Dagman node name (See :pr:`53`)


Version 0.1.4 (2017-06-08)
--------------------------

**Changes**:

* Fixes bug where Jobs that have no arguments, when submitted from a Dagman, were not included in the dag submit file. (See :issue:`33`)


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
