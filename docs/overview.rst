.. _overview:

:github_url: https://github.com/jrbourbeau/pycondor

--------
Overview
--------

The primary functionality of PyCondor is implemented in the **Job** and
**Dagman** objects.

Job objects represent an executable (e.g. a shell command, Python script, etc.)
that you would like to run on an HTCondor cluster. While Dagman (short for
directed acyclic graph manager) objects are a collection of Jobs to be run. In
addition to acting as a collection of Jobs, Dagman objects also allow you to

- Specify dependencies between Jobs (e.g. parent / child relationships)
- Retry failed Jobs
- Throttle the number of running Jobs
- Etc.

These features, in particular specifying inter-job dependencies, allow for the
construction of complex workflows.


Why PyCondor?
-------------

`HTCondor <https://research.cs.wisc.edu/htcondor/>`_ is a an open-source
workload management system for high-throughput computing tasks. It's an
incredibly useful and versatile tool. However, the process of submitting jobs
to HTCondor, especially in complex worflows where there are inter-job
dependencies, can quickly become both tedious and intricate. PyCondor helps
streamline the job submission process by providing

- A simple, user-friendly API
- Built-in functionality to automate common tasks
- Familiar terminology

For a walkthrough of an example workflow using PyCondor see the
:doc:`PyCondor tutorial <tutorial>` page.  
