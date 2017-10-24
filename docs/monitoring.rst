.. monitoring:

:github_url: https://github.com/jrbourbeau/pycondor

*****************
Dagman Monitoring
*****************

PyCondor comes with a command line tool, ``dagman_progress``, to display a
progress bar for Dagman jobs in the terminal. This can be useful for long
running Dagman processes.

.. code-block:: shell

    $ dagman_progress /path/to/dagman/submit_file.submit
    [##############################] 100% Done | 89 done, 0 queued, 0 ready, 0 unready, 0 failed | 51.3m

``dagman_progress`` displays:

* A progress bar indicating the percent of all jobs that are marked as done.

* The number of jobs that are done, queued, ready, unready, and failed.

* The duration the Dagman has been running (in minutes).
