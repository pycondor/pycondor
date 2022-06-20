.. _environment-variables:

:github_url: https://github.com/pycondor/pycondor

*******************************************************
Specifying file directories using environment variables
*******************************************************

One way to specify where the submit, log, output, and error files for a Job
should be written is by using the ``submit``, ``log``, ``output``, and
``error`` Job parameters. For example,

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


Alternatively, these directories can also be specified by defining
``PYCONDOR_SUBMIT_DIR``, ``PYCONDOR_ERROR_DIR``, ``PYCONDOR_LOG_DIR``, and
``PYCONDOR_OUTPUT_DIR`` environment variables.

If any directories are explicitly passed to a Job, then they will be used over
an environment variable. While if an environment variable is set, and a
directory is not explicitly passed to a Job, then the directory given by
an environment variables will be used.

So the above code is equivalent to

.. code-block:: python

    from pycondor import Job
    import os

    os.environ['PYCONDOR_SUBMIT_DIR'] = os.path.abspath('condor/submit')
    os.environ['PYCONDOR_ERROR_DIR'] = os.path.abspath('condor/error')
    os.environ['PYCONDOR_LOG_DIR'] = os.path.abspath('condor/log')
    os.environ['PYCONDOR_OUTPUT_DIR'] = os.path.abspath('condor/output')

    job = Job(name='sleep_job',
              executable='/bin/sleep')


In addition, if you've specified these environment variables in your shell via

.. code-block:: bash

    export PYCONDOR_SUBMIT_DIR="condor/submit"
    export PYCONDOR_ERROR_DIR="condor/error"
    export PYCONDOR_LOG_DIR="condor/log"
    export PYCONDOR_OUTPUT_DIR="condor/output"


then above Jobs are equivalent to

.. code-block:: python

    from pycondor import Job

    job = Job(name='sleep_job',
              executable='/bin/sleep')
