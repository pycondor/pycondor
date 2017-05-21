# Release Notes

## Version 0.1.2

**Changes**:

* Adds `retry` option to the Job `add_arg` method. This allows the user to
specify the number of times to re-submit this node in the Job if the node fails.
* Adds `name` option to the Job `add_arg` method. If a name is specified, then a
separate set of log, output, and error files will be generated specifically for
that node.


## Version 0.1.1

**Changes**:

* Adds `use_unique_id` option when creating a Job object. This will then create a separate error, log, and output file for each of the arguments in the Job `args` list.
* Adds `extra_lines` option when creating a Dagman object (similar to the Job object).
* Replaces all occurances of `os.system()` with `subprocess.Popen()`. This won't affect anything the user touches, just modernizing under-the-hood stuff.


## Version 0.1.0

**Changes**:

* Adds `request_cpus` attribute to Job object to make it easier to request a specified number of CPUs.
* Adds `pycondor.get_queue()` feature to get `condor_q` information.
* Job and Dagman object methods now return `self`.
* Fixed typo in logger formatting.
