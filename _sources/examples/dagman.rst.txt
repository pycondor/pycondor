.. _dagman:

:github_url: https://github.com/jrbourbeau/pycondor

*****************
Creating a Dagman
*****************

We'll assume we've defined paths to the directories where we'd like our
submit, log, output, and error files to be written.

.. code-block:: python

    error = ...
    output = ...
    log = ...
    submit = ...

We can construct a Dagman by creating an instance of the ``Dagman`` class with a
name and directory in which to write the corresponding Dagman submit file to.

.. code-block:: python

    from pycondor import Dagman

    dagman = Dagman(name='example_dagman',
                    submit=submit)


Next, we'll need to add Jobs to our Dagman. This can be done by passing a
Dagman object to the ``dag`` parameter when instantiating a Job.

.. code-block:: python

    from pycondor import Job

    # Instantiate Jobs
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
    job_sleep.add_arg('1')
    job_sleep.add_arg('2')
    job_sleep.add_arg('3')


Alternatively, instead of using the ``dag`` parameter when instantiating a Job,
Dagman objects have an ``add_job`` method that can be used to add Jobs to a
Dagman. I.e. ``dagman.add_job(job)`` is another way to add a Job to a Dagman.
See the :ref:`Dagman API documentation <dagman-api>` for more information.


Finally we can call the Dagman ``build_submit`` method to write all necessary
submit files and submit the Dagman to HTCondor.

.. code-block:: python

    dagman.build_submit()
