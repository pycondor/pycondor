
```
Dagman(name, submit=cwd, extra_lines=None, verbose=0)
```

The `Dagman` object acts as a container for `Job` objects. `Dagman` objects also handle any inter-job dependencies, such as parent-child relationships between jobs.


### Parameters

* `name` : `str`

    Name of the Dagman instance. This will also be the name of the corresponding error, log, output, and submit files associated with this Dagman.

* `submit` : `str` (default: current directory)

    Path to directory where condor dagman submit files will be written. (Defaults to the directory was the job was submitted from).

* `extra_lines` : `list` (default: `None`)

    List of additional lines to be added to submit file.

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

    *Returns:*

    * `self` : `Job`

        Returns self.

* `build(makedirs, fancyname)`

    *Parameters:*

    * `makedirs` : `bool` (default: `True`)

        If specified Dagman and/or Job directories (e.g. error, output, log, submit) don't exist, create them.

    * `fancyname` : `bool` (default: `True`)

        Appends the date and unique id number to error, log, output, and submit files. For example, instead of `jobname.submit` the submit file becomes `jobname_YYYYMMD_id`. This is useful when running several Jobs of the same name.

    *Returns:*

    * `self` : `Job`

        Returns self.


* `submit_dag(kwargs)`

    *Parameters:*

    * `kwargs` : `dict` (default: `{}`)

        Any additional options you would like specified when `condor_submit_dag` is called (see HTCondor [documentation](http://research.cs.wisc.edu/htcondor/manual/current/condor_submit_dag.html) for possible options). For example, if you would like to add `-maxjobs 1000` to the `condor_submit_dag` command, then `kwargs = {'-maxjobs': 1000}`.

* `build_submit(makedirs, fancyname, kwargs)`

    Convenience method. First calls `build()` then `submit_dag()`, with appropriate arguments.
