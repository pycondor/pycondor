
import os
import pytest
from pycondor import Job
from pycondor.tests.utils import clear_pycondor_environment_variables

clear_pycondor_environment_variables()


def test_add_arg_type_fail():
    with pytest.raises(TypeError) as excinfo:
        job = Job('jobname', 'jobex')
        job.add_arg(50)
    error = 'arg must be a string'
    assert error == str(excinfo.value)


def test_add_arg_name_type_fail():
    with pytest.raises(TypeError) as excinfo:
        job = Job('jobname', 'jobex')
        job.add_arg('arg', name=23.12)
    error = 'name must be a string'
    assert error == str(excinfo.value)


def test_add_arg_retry_type_fail():
    with pytest.raises(TypeError) as excinfo:
        job = Job('jobname', 'jobex')
        job.add_arg('arg', retry='10')
    error = 'retry must be an int'
    assert error == str(excinfo.value)


def test_add_child_type_fail():
    with pytest.raises(TypeError) as excinfo:
        job = Job('jobname', 'jobex')
        job.add_child('childjob')
    error = 'add_child() is expecting a Job or Dagman instance. ' + \
            'Got an object of type {}'.format(type('childjob'))
    assert error == str(excinfo.value)


def test_add_children_type_fail():
    with pytest.raises(TypeError):
        job = Job('jobname', 'jobex')
        job.add_children([1, 2, 3, 4])


def test_add_parent_type_fail():
    with pytest.raises(TypeError) as excinfo:
        job = Job('jobname', 'jobex')
        job.add_parent('parentjob')
    error = 'add_parent() is expecting a Job or Dagman instance. ' + \
            'Got an object of type {}'.format(type('parentjob'))
    assert error == str(excinfo.value)


def test_add_parents_type_fail():
    with pytest.raises(TypeError):
        job = Job('jobname', 'jobex')
        job.add_parents([1, 2, 3, 4])


def test_build_executeable_not_found_fail():
    with pytest.raises(IOError) as excinfo:
        ex = '/path/to/executable'
        job = Job('jobname', ex)
        job.build(makedirs=False)
    error = 'The executable {} does not exist'.format(ex)
    assert error == str(excinfo.value)


def test_queue_written_to_submit_file(tmpdir):
    # Test to check that the queue parameter is properly written
    # to submit file when Job is created. See issue #38.

    example_script = os.path.join('examples/savelist.py')

    submit_dir = str(tmpdir.mkdir('submit'))

    # Build Job object with queue=5
    job = Job('jobname', example_script, submit=submit_dir, queue=5)
    job.build(fancyname=False)

    # Read the built submit file and check that the 'queue 5' is
    # contained in the file.
    with open(job.submit_file, 'r') as f:
        lines = f.readlines()
    assert 'queue 5' in lines


def test_job_env_variable_dir(tmpdir):
    # Set pycondor environment variables
    for dir_name in ['submit', 'output', 'error', 'log']:
        dir_path = str(tmpdir.mkdir(dir_name))
        os.environ['PYCONDOR_{}_DIR'.format(dir_name.upper())] = dir_path

    example_script = os.path.join('examples/savelist.py')
    job = Job('jobname', example_script)
    job.build()
    for dir_name in ['submit', 'output', 'error', 'log']:
        tmpdir_path = os.path.join(str(tmpdir), dir_name)
        job_path = os.path.dirname(getattr(job, '{}_file'.format(dir_name)))
        assert tmpdir_path == job_path

    clear_pycondor_environment_variables()
