.. _basic-job-example:

:github_url: https://github.com/jrbourbeau/pycondor

**************
Creating a Job
**************

One of the basic building blocks of PyCondor is the Job object. A Job object
represents an executable (e.g. a shell command, Python script, etc.) that you
would like to run using HTCondor.


.. code-block:: python

    from pycondor import Job


We will need to define the directories where we would like PyCondor to save
the submit file, log file, standard output file, and standard error file
associated with running a Job.

.. code-block:: python

    import os

    error = os.path.abspath('condor/error')
    output = os.path.abspath('condor/output')
    log = os.path.abspath('condor/log')
    submit = os.path.abspath('condor/submit')


Now we can instantiate a Job object by providing a name, executable, and
specifying where files should be written to.

.. code-block:: python

    job = Job(name='sleep_job',
              executable='/bin/sleep',
              submit=submit,
              error=error,
              output=output,
              log=log)


Finally we can use the ``build_submit`` method to build the submit file for
this Job and submit it to HTCondor.

.. code-block:: python

    job.build_submit()
