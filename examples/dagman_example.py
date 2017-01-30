#!/usr/bin/env python

import pycondor

if __name__ == "__main__":

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
