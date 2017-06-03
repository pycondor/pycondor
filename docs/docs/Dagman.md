
```python
Dagman(name, submit=cwd, extra_lines=None, verbose=0)
```

The `Dagman` object acts as a container for `Job`  and other `Dagman` objects. `Dagman` objects also handle any inter-job dependencies, such as parent-child relationships between `Jobs` and other `Dagmans`.


### Parameters

* `name` : `str`

    Name of the Dagman instance. This will also be the name of the corresponding error, log, output, and submit files associated with this Dagman.

* `submit` : `str` (default: current directory)

    Path to directory where condor dagman submit files will be written. (Defaults to the directory was the job was submitted from).

* `extra_lines` : `list` (default: `None`)

    *(Added in version 0.1.1)*

    List of additional lines to be added to submit file.

* `verbose` : `int` (default: 0)

    Level of logging verbosity.

    * 0 &mdash; warning (least verbose)
    * 1 &mdash; info
    * 2 &mdash; debug (most verbose)

### Attributes

* `nodes` : `list` (default: `[]`)

    List of Job and other Dagman objects to be included in Dagman submit file.


* `parents` : `list` (default: `[]`)

    *(Added in version 0.1.3)*

    List of parent Jobs and Dagmans. Ensures that Jobs and other Dagmans in the parents list will complete before this Dagman is submitted to HTCondor.


* `children` : `list` (default: `[]`)

    *(Added in version 0.1.3)*

    List of children Jobs and Dagmans. Ensures that Jobs and other Dagmans in the children list will be submitted after this Dagman is has completed.



### Methods

* `add_job(job)`

    *Parameters:*

    * `job` : `Job`

        Job to append to the `nodes` list.

    *Returns:*

    * `self` : `Dagman`

        Returns self.

* `add_subdag(dag)`

    *Parameters:*

    * `dag` : `Dagman`

        Dagman to append to the `nodes` list.

    *Returns:*

    * `self` : `Dagman`

        Returns self.


* `add_parent(object)`

    *Parameters:*

    * `object` : `Job`, `Dagman`

        Job or Dagman to append to the `parents` list.

    *Returns:*

    * `self` : `Job`, `Dagman`

        Returns self.


* `add_child(object)`

    *Parameters:*

    * `object` : `Job`

        Job or Dagman to append to the `children` list.

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

    * `self` : `Dagman`

        Returns self.


* `submit_dag(kwargs)`

    *Parameters:*

    * `kwargs` : `dict` (default: `{}`)

        Any additional options you would like specified when `condor_submit_dag` is called (see HTCondor [documentation](http://research.cs.wisc.edu/htcondor/manual/current/condor_submit_dag.html) for possible options). For example, if you would like to add `-maxjobs 1000` to the `condor_submit_dag` command, then `kwargs = {'-maxjobs': 1000}`.

* `build_submit(makedirs, fancyname, kwargs)`

    Convenience method. First calls `build()` then `submit_dag()`, with appropriate arguments.
