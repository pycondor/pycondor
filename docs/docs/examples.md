# Examples

All of the following examples use a dummy script, `savelist.py`, that creates and saves a Python `list`. `savelist.py` has a command-line argument `--length` that specifies how many items to generate in the list (default: 10). The script is located in the `examples/` directory in the [PyCondor repository](https://github.com/jrbourbeau/pycondor).

## Job examples

### Basic Job submission

```
import pycondor

# Declare the error, output, log, and submit directories for Condor Job
error = 'condor/error'
output = 'condor/output'
log = 'condor/log'
submit = 'condor/submit'

# Setting up a PyCondor Job
job = pycondor.Job('examplejob', 'savelist.py',
               error=error, output=output,
               log=log, submit=submit, verbose=2)
# Write all necessary submit files and submit job to Condor
job.build_submit()
```


### Adding arguments to a Job

```

import pycondor

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
# Write all necessary submit files and submit job to Condor
job.build_submit()

```
---

## Dagman examples


### Adding Jobs to a Dagman
```
import pycondor

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
```

### Add inter-job dependencies

```
import pycondor

# Declare the error, output, log, and submit directories for Condor Job
error = 'condor/error'
output = 'condor/output'
log = 'condor/log'
submit = 'condor/submit'

# Setting up first PyCondor Job
job1 = pycondor.Job('examplejob1', 'savelist.py',
               error=error, output=output,
               log=log, submit=submit, verbose=2)
# Adding arguments to job1
job1.add_arg('--length 100')
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
```
