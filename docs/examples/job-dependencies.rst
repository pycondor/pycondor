.. _job-dependencies:

:github_url: https://github.com/jrbourbeau/pycondor

*****************************
Adding Inter-Job Dependencies
*****************************

Note that specifying inter-job dependencies is a Dagman feature and can only
be done when Jobs are being submitted via a Dagman. We'll assume we've defined
paths to the directories where we'd like our submit, log, etc. files to be
written to.

.. code-block:: python

    error = ...
    output = ...
    log = ...
    submit = ...


We can define a Dagman

.. code-block:: python

    from pycondor import Dagman

    dagman = Dagman(name='example_dagman',
                    submit=submit)


and add Jobs to the Dagman

.. code-block:: python

    job_date = Job(name='date_job',
                   executable='/bin/date',
                   submit=submit,
                   error=error,
                   output=output,
                   log=log,
                   dag=dagman)

    job_sleep = Job(name='sleep_job',
                    executable='/bin/sleep',
                    submit=submit,
                    error=error,
                    output=output,
                    log=log,
                    dag=dagman)


as outlined in the :doc:`basic-job` and :doc:`dagman` examples. Next we can
add inter-job relationships using the Job ``add_child`` and
``add_parent`` methods. For example,

.. code-block:: python

    job_date.add_child(job_sleep)

adds ``job_sleep`` as a child job to ``job_date``. This dependency ensures that
``job_sleep`` will not be submitted to HTCondor until after ``job_date`` is
complete.

Note that instead of using the ``add_child`` method as above, the same
dependency can be specified using the ``add_parent`` method. In other words,

.. code-block:: python

    job_sleep.add_parent(job_date)


is equivalent to ``job_date.add_child(job_sleep)``.

.. code-block:: python

    dagman.build_submit()
