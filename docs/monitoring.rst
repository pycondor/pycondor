.. monitoring:

:github_url: https://github.com/jrbourbeau/pycondor

**********************
Command line interface
**********************

-----------------
Dagman Monitoring
-----------------

PyCondor comes with a ``dagman_progress`` command, to display a
progress bar for Dagman jobs in the terminal. This can be useful for long
running Dagman processes.

.. code-block:: shell

    $ dagman_progress /path/to/dagman/submit_file.submit
    [##############################] 100% Done | 89 done, 0 queued, 0 ready, 0 unready, 0 failed | 51.3m

``dagman_progress`` displays:

* A progress bar indicating the percent of all jobs that are marked as done.

* The number of jobs that are done, queued, ready, unready, and failed.

* The duration the Dagman has been running (in minutes).


---------------------------
Command line Job submission
---------------------------

PyCondor comes with a ``pycondor_submit`` command to easily submit Jobs to
HTCondor directly from the command line. This can be useful for testing and
debugging. For example,

.. code-block:: shell

    $ pycondor_submit --executable my_script.py

The ``pycondor_submit`` command accepts several options. For example, to
requesting a specified amount of memory

.. code-block:: shell

    $ pycondor_submit --request_memory 3GB --executable my_script.py

or to write log files to a specified directory

.. code-block:: shell

    $ pycondor_submit --log /path/to/log_dir --executable my_script.py

See ``pycondor_submit --help`` for more information.
