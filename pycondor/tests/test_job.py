
import os
import pytest
import pycondor


def test_add_arg_int_fail():
    with pytest.raises(ValueError) as excinfo:
        job = pycondor.Job('jobname', 'jobex')
        job.add_arg(50)
    error = 'arg must be a string'
    assert error == str(excinfo.value)


def test_add_arg_name_float_fail():
    with pytest.raises(ValueError) as excinfo:
        job = pycondor.Job('jobname', 'jobex')
        job.add_arg('arg', name=23.12)
    error = 'name must be a string'
    assert error == str(excinfo.value)


def test_add_arg_retry_string_fail():
    with pytest.raises(ValueError) as excinfo:
        job = pycondor.Job('jobname', 'jobex')
        job.add_arg('arg', retry='10')
    error = 'retry must be an int'
    assert error == str(excinfo.value)


def test_add_child_fail():
    with pytest.raises(ValueError) as excinfo:
        job = pycondor.Job('jobname', 'jobex')
        job.add_child('childjob')
    error = 'add_child() is expecting a Job or Dagman instance. ' + \
            'Got an object of type {}'.format(type('childjob'))
    assert error == str(excinfo.value)


def test_add_parent_fail():
    with pytest.raises(ValueError) as excinfo:
        job = pycondor.Job('jobname', 'jobex')
        job.add_parent('parentjob')
    error = 'add_parent() is expecting a Job or Dagman instance. ' + \
            'Got an object of type {}'.format(type('parentjob'))
    assert error == str(excinfo.value)


def test_build_executeable_not_found_fail():
    with pytest.raises(IOError) as excinfo:
        ex = '/path/to/executable'
        job = pycondor.Job('jobname', ex)
        job.build(makedirs=False)
    error = 'The path {} does not exist'.format(ex)
    assert error == str(excinfo.value)


def test_queue_written_to_submit_file(tmpdir):
    # Test to check that the queue parameter is properly written
    # to submit file when Job is created. See issue #38.

    example_script = os.path.join('examples/savelist.py')

    submit_dir = str(tmpdir.mkdir('submit'))

    # Build Job object with queue=5
    job = pycondor.Job('jobname', example_script,
                       submit=submit_dir, queue=5)
    job.build(fancyname=False)

    # Read the built submit file and check that the 'queue 5' is
    # contained in the file.
    with open(job.submit_file, 'r') as f:
        lines = f.readlines()
    assert 'queue 5' in lines
