.. _examples:
:github_url: https://github.com/jrbourbeau/pycondor

********
Examples
********

All of the following examples use a dummy script, ``savelist.py``, that creates and saves a Python ``list``. ``savelist.py`` has a command-line argument ``--length`` that specifies how many items to generate in the list (default: ``10``). The script is located in the ``examples/`` directory in the `PyCondor repository <https://github.com/jrbourbeau/pycondor>`_.


============
Job examples
============
--------------------
Basic Job submission
--------------------

.. code-block:: python

    import pycondor

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up a PyCondor Job
    job = pycondor.Job('examplejob', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Write all necessary submit files and submit job to Condor
    job.build_submit()

-------------------------
Adding arguments to a Job
-------------------------

.. code-block:: python

    import pycondor

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up a PyCondor Job
    job = pycondor.Job('examplejob', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job
    job.add_arg('--length 50')
    job.add_arg('--length 100')
    job.add_arg('--length 200')
    # Write all necessary submit files and submit job to Condor
    job.build_submit()


===============
Dagman examples
===============

-----------------------
Adding Jobs to a Dagman
-----------------------

.. code-block:: python

    import pycondor

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up a PyCondor Job
    job = pycondor.Job('examplejob', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job
    job.add_arg('--length 50')
    job.add_arg('--length 100')
    job.add_arg('--length 200')

    # Setting up a PyCondor Dagman
    dagman = pycondor.Dagman('exampledagman', submit=submit, verbose=2)
    # Add job to dagman
    dagman.add_job(job)
    # Write all necessary submit files and submit job to Condor
    dagman.build_submit()

--------------------------
Add inter-job dependencies
--------------------------

.. code-block:: python

    import pycondor

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up first PyCondor Job
    job1 = pycondor.Job('examplejob1', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job1
    job1.add_arg('--length 100')
    # Setting up second PyCondor Job
    job2 = pycondor.Job('examplejob2', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job1
    job2.add_arg('--length 200')

    # Add interjob reltionship.
    # Ensure that job1 is complete before job2 starts
    job1.add_child(job2)

    # Setting up a PyCondor Dagman
    dagman = pycondor.Dagman('exampledagman', submit=submit, verbose=2)
    # Add jobs to dagman
    dagman.add_job(job1)
    dagman.add_job(job2)
    # Write all necessary submit files and submit job to Condor
    dagman.build_submit()

------------------------
A Dagman within a Dagman
------------------------

.. code-block:: python

    import pycondor

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up first PyCondor Job
    job1 = pycondor.Job('examplejob1', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job1
    for i in range(10, 100, 10):
        job1.add_arg('--length {}'.format(i), retry=7)

    # Setting up second PyCondor Job
    job2 = pycondor.Job('examplejob2', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job1
    job2.add_arg('--length 200', name='200jobname')
    job2.add_arg('--length 400', name='400jobname', retry=3)

    # Setting up a PyCondor Dagman
    subdag = pycondor.Dagman('example_subdag', submit=submit, verbose=2)
    # Add job1 to dagman
    subdag.add_job(job1)
    subdag.add_job(job2)

    # Setting up third PyCondor Job
    job3 = pycondor.Job('examplejob3', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, verbose=2)
    # Adding arguments to job1
    for length in range(210, 220):
        job3.add_arg('--length {}'.format(length))

    # Add interjob reltionship.
    # Ensure that the subdag is complete before job3 starts
    subdag.add_child(job3)

    # Setting up a PyCondor Dagman
    dagman = pycondor.Dagman('exampledagman', submit=submit, verbose=2)
    # Add jobs to dagman
    dagman.add_job(job3)
    dagman.add_subdag(subdag)
    # Write all necessary submit files and submit job to Condor
    dagman.build_submit()
