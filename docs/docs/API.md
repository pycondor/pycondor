<a id='top'> </a>

# PyCondor API

PyCondor consists of two objects, the `Job` object and the `Dagman` object.

The `Job` object consists of an executable to run on Condor, any specifications to include in the corresponding submit file (e.g. memory request, universe execution environment, etc.), and any arguments that you would like to pass to the executable. `Job` objects can be submitted directly to HTCondor, or can be included in a `Dagman` object for additional job management functionality.

The `Dagman` object acts as a container for `Job` objects. `Dagman` objects also handle any inter-job dependencies, such as parent-child relationships between jobs.


## Job

**Job(name, executable, error=None, log=None, output=None, submit=cwd, request_memory=None, request_disk=None, request_cpus=None, getenv=True, universe='vanilla', initialdir=None, notification='never', requirements=None, queue=None, extra_lines=None, verbose=0)**


### Parameters

* `name` : `str`

    Name of the Job instance. This will also be the name of the corresponding error, log, output, and submit files associated with this job.

* `executable` : `str`

    Path to corresponding executable for Job.

* `error` : `str` (default: `None`)

    Path to directory where condor job error files will be written.

* `log` : `str` (default: `None`)

    Path to directory where condor job log files will be written.

* `output` : `str` (default: `None`)

    Path to directory where condor job output files will be written.

* `submit` : `str` (default: current directory)

    Path to directory where condor job submit files will be written. (Defaults to the directory was the job was submitted from).

* `request_memory` : `str` (default: `None`)

    Memory request to be included in submit file.

* `request_disk` : `str` (default: `None`)

    Disk request to be included in submit file.

* `request_cpus` : `int` (default: `None`)

    *(Added in version 0.0.2)*

    Number of CPUs to request in submit file.

* `getenv` : `bool` (default: `True`)

    Whether or not to use the current environment settings when running the job.

* `universe` : `str` (default: `'vanilla'`)

    Universe execution environment to be specified in submit file.

* `initialdir` : `str` (default: `None`)

    Initial directory for relative paths (defaults to the directory was the job was submitted from).

* `notification` : `str` (default: `'never'`)

    E-mail notification preference.

* `requirements` : `str` (default: `None`)

    Additional requirements to be included in ClassAd.

* `queue` : `int` (default: `None`)

    Integer specifying how many times you would like this job to run.

* `extra_lines` : `list` (default: `None`)

    List of additional lines to be added to submit file.

* `verbose` : `int` (default: 0)

    Level of logging verbosity.

    * 0 &mdash; warning (least verbose)
    * 1 &mdash; info
    * 2 &mdash; debug (most verbose)


### Attributes

* `args` : `list` (default: `[]`)

    List of command-line arguments that will be passed to the Job executable.

* `parents` : `list` (default: `[]`)

    *Only applies when Job is in a Dagman*. List of parent Jobs. Dagman will ensure that Jobs in the parents list will complete before this Job is submitted to HTCondor.

* `children` : `list` (default: `[]`)

    *Only applies when Job is in a Dagman*. List of child Jobs. Dagman will ensure that Jobs in the children list will be submitted to HTCondor only after this Job has completed.

* `prescript` : `Script` (default: `None`)

    *(Added in version 0.0.2)*

    *Only applies when Job is in a Dagman*. Script to run before Job.

* `postscript` : `Script` (default: `None`)

    *(Added in version 0.0.2)*

    *Only applies when Job is in a Dagman*. Script to run after Job.


### Methods

* `add_arg(arg)`

    *Parameters:*

    * `arg` : `str`

        Argument to append to Job `args` list.

* `add_parent(job)`

    *Parameters:*

    * `job` : `Job`

        Job to append to the `parents` list.

* `add_child(job)`

    *Parameters:*

    * `job` : `Job`

        Job to append to the `children` list.

* `add_prescript(executable, args, apply_each)`

    *(Added in version 0.0.2)*

    *Parameters:*

    * `executable` : `str`

        Path to executable script.

    * `args` : `str` (default: `None`)

        Any command-line arguments that you would like to pass to `executable`.

    * `apply_each` : `bool` (default: `False`)

        Whether or not to apply the pre-script to each HTCondor job associated with this Job.

* `add_postscript(executable, args, apply_each)`

    *(Added in version 0.0.2)*

    *Parameters:*

    * `executable` : `str`

        Path to executable script.

    * `args` : `str` (default: `None`)

        Any command-line arguments that you would like to pass to `executable`.

    * `apply_each` : `bool` (default: `False`)

        Whether or not to apply the post-script to each HTCondor job associated with this Job.

* `build(makedirs, fancyname)`

    *Parameters:*

    * `makedirs` : `bool` (default: `True`)

        If specified Job directories (e.g. error, output, log, submit) don't exist, create them.

    * `fancyname` : `bool` (default: `True`)

        Appends the date and unique id number to error, log, output, and submit files. For example, instead of `jobname.submit` the submit file becomes `jobname_YYYYMMD_id`. This is useful when running several Jobs of the same name.

* `submit_job(kwargs)`

    *Parameters:*

    * `kwargs` : `dict` (default: `{}`)

        Any additional options you would like specified when `condor_submit` is called (see HTCondor [documentation](http://research.cs.wisc.edu/htcondor/manual/current/condor_submit.html) for possible options). For example, if you would like to add `-maxjobs 1000` to the `condor_submit` command, then `kwargs = {'-maxjobs': 1000}`.

* `build_submit(makedirs, fancyname, kwargs)`

    Convenience method. First calls `build()` then `submit_job()`, with appropriate arguments.


## Dagman
[ [back to top](#top) ]

**Dagman(name, submit=cwd, verbose=0)**

### Parameters

* `name` : `str`

    Name of the Dagman instance. This will also be the name of the corresponding error, log, output, and submit files associated with this Dagman.

* `submit` : `str` (default: current directory)

    Path to directory where condor dagman submit files will be written. (Defaults to the directory was the job was submitted from).

* `verbose` : `int` (default: 0)

    Level of logging verbosity.

    * 0 &mdash; warning (least verbose)
    * 1 &mdash; info
    * 2 &mdash; debug (most verbose)

### Attributes

* `jobs` : `list` (default: `[]`)

    List of Job objects to be included in DAGMan submit file.

### Methods

* `add_job(job)`

    *Parameters:*

    * `job` : `Job`

        Job to append to the `jobs` list.

* `build(makedirs, fancyname)`

    *Parameters:*

    * `makedirs` : `bool` (default: `True`)

        If specified Dagman and/or Job directories (e.g. error, output, log, submit) don't exist, create them.

    * `fancyname` : `bool` (default: `True`)

        Appends the date and unique id number to error, log, output, and submit files. For example, instead of `jobname.submit` the submit file becomes `jobname_YYYYMMD_id`. This is useful when running several Jobs of the same name.

* `submit_dag(kwargs)`

    *Parameters:*

    * `kwargs` : `dict` (default: `{}`)

        Any additional options you would like specified when `condor_submit_dag` is called (see HTCondor [documentation](http://research.cs.wisc.edu/htcondor/manual/current/condor_submit_dag.html) for possible options). For example, if you would like to add `-maxjobs 1000` to the `condor_submit_dag` command, then `kwargs = {'-maxjobs': 1000}`.

* `build_submit(makedirs, fancyname, kwargs)`

    Convenience method. First calls `build()` then `submit_dag()`, with appropriate arguments.
