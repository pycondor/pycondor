# Welcome to the PyCondor documentation

[PyCondor](https://github.com/jrbourbeau/pycondor) (Python HTCondor) is a tool that helps build and submit HTCondor jobs in a straight-forward manner with minimal hassle.

## Motivation

[HTCondor](https://research.cs.wisc.edu/htcondor/) is a an open-source workload management system for high-throughput computing tasks developed at the University of Wisconsin–Madison. It is an incredibly useful and versatile tool. However, the process of submitting jobs to HTCondor, especially when there are inter-job dependencies, can quickly become both tedious and complex. PyCondor is a tool to help streamline this job submission process through a user-friendly API and built-in functionality to automate common tasks.

## Useful Links

* Documentation: [http://www.jamesbourbeau.com/pycondor](http://www.jamesbourbeau.com/pycondor)
* GitHub repository: [https://github.com/jrbourbeau/pycondor](https://github.com/jrbourbeau/pycondor)
* PyPI: [https://pypi.python.org/pypi/PyCondor](https://pypi.python.org/pypi/PyCondor)
* Issue tracker: [https://github.com/jrbourbeau/pycondor/issues](https://github.com/jrbourbeau/pycondor/issues)


## Example

With just a couple lines of code, you can get PyCondor up and running!

```python
import pycondor

# Setting up a PyCondor Job
job = pycondor.Job('examplejob', 'script.py')
# Write all necessary submit files and submit job to Condor
job.build_submit()
```
