.. _tutorial:

:github_url: https://github.com/jrbourbeau/pycondor

********
Tutorial
********

This tutorial walks through the example workflow shown below. This tutorial script can be found in the `PyCondor examples on GitHub <https://github.com/jrbourbeau/pycondor/blob/master/examples/tutorial.py>`_.

.. code-block:: python

    from pycondor import Job, Dagman

    # Define the error, output, log, and submit directories
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Instantiate a Dagman
    dagman = Dagman(name='tutorial_dagman',
                    submit=submit)

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

    # Add inter-job relationship
    # Ensure that job_sleep finishes before job_date starts
    job_sleep.add_child(job_date)

    # Write all necessary submit files and submit job to HTCondor
    dagman.build_submit()


----------------------
Job and Dagman objects
----------------------

The basic building blocks in PyCondor are the Job and Dagman objects. A Job object represents an executable (e.g. a shell command, Python script, etc.) that you would like to run using HTCondor. While the Dagman object represents a collection of Job objects to run.

.. code-block:: python

    from pycondor import Job, Dagman


Both the Job and Dagman objects can be imported directly from ``pycondor``.


-------------------------------
Job and Dagman file directories
-------------------------------

There are several files associated with both Job and Dagman objects. For each Job and Dagman object, PyCondor will create a submit file. This file will be formatted such that it can be submitted to HTCondor for execution. In addition to submit files, there will also be log files, standard output files, and standard error files associated with running a Job and/or Dagman.

.. code-block:: python

    # Define the error, output, log, and submit directories
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

For this tutorial, we have explicitly specified the directories that we would like the error, output, log, and submit files to be saved to. However, these directories can also be specified by setting the ``PYCONDOR_SUBMIT_DIR``, ``PYCONDOR_ERROR_DIR``, ``PYCONDOR_LOG_DIR``, and ``PYCONDOR_OUTPUT_DIR`` environment variables. For example, setting ``PYCONDOR_SUBMIT_DIR=condor/submit`` is equivalent to the above.


-------------------
Setting up a Dagman
-------------------

The Dagman (short for directed acyclic graph manager) object is a collection of Job objects to be run.

.. code-block:: python

    # Instantiate a Dagman
    dagman = Dagman(name='tutorial_dagman',
                    submit=submit)

For a Dagman, only a ``name`` has to be provided (used to construct the submit, log, etc. file names). In this example a ``submit`` parameter, the path to the directory where the Dagman submit file will be saved, is also provided.

---------------
Setting up Jobs
---------------

Now we're ready to add some Job objects to the Dagman. Both a ``name`` and an ``executable`` must be provided to create a Job.

.. code-block:: python

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

In this example, ``job_date`` will run the shell ``date`` command, and ``job_sleep`` will run the shell ``sleep`` command. A Job can be added to a Dagman object by passing a Dagman to the Job ``dag`` parameter.

In addition to defining an executable for a Job to run, you can also pass arguments to the executable using the Job ``add_arg`` method. Here, we've added three arguments, ``1``, ``2``, and ``3``, to ``job_sleep``. This Job will now run the ``sleep`` command on each of the provided arguments, i.e. ``sleep 1``, ``sleep 2``, and ``sleep 3``.


------------------------------
Adding inter-job relationships
------------------------------

One useful feature of Dagman objects is they can support inter-job relationships between the Jobs they manage.

.. code-block:: python

    # Add inter-job relationship
    # Ensure that job_sleep finishes before job_date starts
    job_sleep.add_child(job_date)

In many workflows, there are dependencies between different Jobs. For example, you might want to make sure one Job finishes before another Job begins. Inter-job relationships in PyCondor can be specified using the Job ``add_child`` and ``add_parent`` methods.

For this tutorial, ``job_sleep.add_child(job_date)`` sets ``job_date`` as a child Job of ``job_sleep``. This means that ``job_date`` will start running only after ``job_sleep`` has finished. Note that ``job_sleep.add_child(job_date)`` is equivalent to ``job_date.add_parent(job_sleep)``.


-----------------------
Build and submit Dagman
-----------------------

Now that the workflow for this tutorial has been set up, we can build all the appropriate Job and Dagman submit files and submit them to HTCondor for execution.


.. code-block:: python

    # Write all necessary submit files and submit job to HTCondor
    dagman.build_submit()


The Dagman ``build_submit`` method is used to both build the appropriate Job and Dagman submit files and then submit them to HTCondor. Note that the ``build_submit`` method is just shorthand for the ``build`` Dagman method followed by the ``submit`` method.


For more examples see the `examples <examples.html>`_ section of the documentation. 
