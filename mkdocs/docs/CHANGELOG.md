# Release Notes

## Version 0.1.0

**Changes**:

* Adds `request_cpus` attribute to Job object to make it easier to request a specified number of CPUs.
* Adds `pycondor.get_queue()` feature to get `condor_q` information. 
* Job and Dagman object methods now return `self`.
* Fixed typo in logger formatting.
