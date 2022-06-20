.. _cli:

:github_url: https://github.com/pycondor/pycondor

************
Command line
************

-----------------
Dagman Monitoring
-----------------

PyCondor comes with a ``pycondor monitor`` command, to display a
progress bar for Dagman jobs in the terminal. This can be useful for long
running Dagman processes.

.. code-block:: shell

    $ pycondor monitor /path/to/dagman/submit_file.submit
    [##############################] 100% Done | 89 done, 0 queued, 0 ready, 0 unready, 0 failed | 51.3m

``pycondor monitor`` displays:

* A progress bar indicating the percent of all jobs that are marked as done.

* The number of jobs that are done, queued, ready, unready, and failed.

* The duration the Dagman has been running (in minutes).

See ``pycondor monitor --help`` for a complete list of available command line options.


---------------------------
Command line Job submission
---------------------------

The ``pycondor submit`` command can be used to easily submit Jobs to
HTCondor directly from the command line. This can be useful for testing and
debugging. For example,

.. code-block:: shell

    $ pycondor submit  my_script.py

The ``pycondor submit`` command accepts several options. For example, to
requesting a specified amount of memory

.. code-block:: shell

    $ pycondor submit --request_memory 3GB  my_script.py

or to write log files to a specified directory

.. code-block:: shell

    $ pycondor submit --log /path/to/log_dir my_script.py

Note that when passing command line arguments to an executable, two dashes (i.e. ``--``)
must be used to separate the ``pycondor submit`` command line arguments from
the command line arguments to be passed to the executable. E.g.

.. code-block:: shell

    $ pycondor submit --request_memory 3GB my_script.py -- --script_option value

See ``pycondor submit --help`` for a complete list of available command line options.

---
API
---

.. click:: pycondor.cli:monitor
   :prog: pycondor monitor
   :show-nested:

.. click:: pycondor.cli:submit
   :prog: pycondor submit
   :show-nested:
