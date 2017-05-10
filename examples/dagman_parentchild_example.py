#!/usr/bin/env python

import pycondor

if __name__ == "__main__":

    # Declare the error, output, log, and submit directories for Condor Job
    error = 'condor/error'
    output = 'condor/output'
    log = 'condor/log'
    submit = 'condor/submit'

    # Setting up first PyCondor Job
    job1 = pycondor.Job('examplejob1', 'savelist.py',
                   error=error, output=output,
                   log=log, submit=submit, use_unique_id=True, verbose=2)
    # Adding arguments to job1
    for i in range(10, 100, 10):
        job1.add_arg('--length {}'.format(i))
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
