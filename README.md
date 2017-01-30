## PyCondor (Python HTCondor)

[HTCondor](https://research.cs.wisc.edu/htcondor/) is a an open-source workload management system for high throughput computing developed at the University of Wisconsin–Madison. PyCondor is a tool that helps **build and submit HTCondor submission files in a straight-forward manner with minimal hassle**.


### Installation

PyCondor can be easily installed via `pip`

`pip install pycondor`

In addition, you can also install PyCondor by downloading the [project package from the Python Package Index](https://pypi.python.org/pypi/PyCondor), unzip the download, navigate to the PyCondor project directory and run

`python setup.py install`



### Examples

For example uses of PyCondor, please see the the `examples/` directory in the project repository.



### API

#### Job

*Job(name, executable, error=None, log=None, output=None, submit=cwd, request_memory=None, request_disk=None, getenv=True, universe='vanilla', initialdir=None, notification='never', requirements=None, queue=None, extra_lines=None, verbose=0)*

**Parameters**:

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


#### Dagman

*Dagman(name, submit=cwd, verbose=0)*

**Parameters**:

* `name` : `str`

    Name of the Dagman instance. This will also be the name of the corresponding error, log, output, and submit files associated with this Dagman.

* `submit` : `str` (default: current directory)

    Path to directory where condor dagman submit files will be written. (Defaults to the directory was the job was submitted from).

* `verbose` : `int` (default: 0)

    Level of logging verbosity.

    * 0 &mdash; warning (least verbose)
    * 1 &mdash; info
    * 2 &mdash; debug (most verbose)


### License

[MIT License](LICENSE)

Copyright (c) 2017 James Bourbeau
