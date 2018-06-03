.. _job-arguments:

:github_url: https://github.com/jrbourbeau/pycondor

********************
Adding Job arguments
********************

First we'll set up a Job similar to the :doc:`basic-job` example.

.. code-block:: python

    from pycondor import Job
    import os

    error = os.path.abspath('condor/error')
    output = os.path.abspath('condor/output')
    log = os.path.abspath('condor/log')
    submit = os.path.abspath('condor/submit')

    job = Job(name='sleep_job',
              executable='/bin/sleep',
              submit=submit,
              error=error,
              output=output,
              log=log)


In addition to running an executable, we might also want to pass several
command line arguments to the executable. This can be facilitated using the
Job ``add_arg`` method.

.. code-block:: python

    job.add_arg('1')
    job.add_arg('2')
    job.add_arg('3')

Here, we've added three arguments, ``1``, ``2``, and ``3``, to ``job``. Now
when this Job is submitted to HTCondor, it will run it's executable (in this
case ``/bin/sleep``) on each of the provided arguments. E.g. ``/bin/sleep 1``,
``/bin/sleep 2``, and ``/bin/sleep 3``.

Note that in this example when this single PyCondor Job is submitted, there
will actually be 3 jobs submitted to HTCondor, one for each of the arguments.

.. code-block:: python

    job.build_submit()
