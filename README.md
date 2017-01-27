## PyCondor (Python HTCondor)

[HTCondor](https://research.cs.wisc.edu/htcondor/) is a an open-source framework for high throughput computing developed at the University of Wisconsin–Madison. It is an extremely useful tool, but the job submission process can be tedious and cumbersome. PyCondor is a tool that helps build and submit HTCondor submission files in a straight-forward manner with minimal hassle.


## Installation

To get PyCondor, just clone the repository via

`git clone https://github.com/jrbourbeau/pycondor.git`

Make sure the path to the PyCondor repository to your system's `PYTHONPATH`.



## Code examples

For example uses of PyCondor, please see the [example Jupyter notebook](#examples.ipynb).



## API

### Job

*Job(name, executable, error=None, log=None, output=None, submit=None, request_memory=None, request_disk=None, getenv=True, universe='vanilla', initialdir=None, notification='never', queue='', extra_lines=None, verbose=0)*

**Parameters**:

* `name` : str

    Name of the Job instance
* `path` : str

    Path to corresponding executable for Job
* `error` : str (default: None)

    Path to directory where condor job error files will be written
* `log` : str (default: None)

    Path to directory where condor job log files will be written
* `output` : str (default: None)

    Path to directory where condor job output files will be written
* `submit` : str (default: None)

    Path to directory where condor job submit files will be written
* `request_memory` : str (default: None)

    Memory request to be included in HTCondor ClassAd
* `request_disk` : str (default: None)

    Memory request to be included in HTCondor ClassAd
* `getenv` : bool (default: True)

    Whether or not to use the current environment settings when running the job.
* `verbose` : int (default: 0)

    Level of logging verbosity. If 0, then no output is logged. If 1, logging level is set to info. If 2, logging level is set to debug.


### Dagman

*Dagman(name, config=None, verbose=0)*

**Parameters**:

* `name` : str

    Name of the Dagman instance
* `submit` : str (default: None)

    Path to directory where DAGMan files (submit, log, out, error, etc.) will be written
* `verbose` : int (default: 0)

    Verbosity level (0, 1, 2 &mdash; 0 is least verbose, 2 is most verbose)


### License

[MIT License](LICENSE)

Copyright (c) 2017 James Bourbeau
