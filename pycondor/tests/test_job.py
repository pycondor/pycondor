
import os
import pytest
from pycondor import Job
from pycondor.utils import clear_pycondor_environment_variables

clear_pycondor_environment_variables()

example_script = os.path.join('examples/savelist.py')


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

    job = Job('jobname', example_script)
    job.build()
    for dir_name in ['submit', 'output', 'error', 'log']:
        tmpdir_path = os.path.join(str(tmpdir), dir_name)
        job_path = os.path.dirname(getattr(job, '{}_file'.format(dir_name)))
        assert tmpdir_path == job_path

    clear_pycondor_environment_variables()


def test_repr():
    default_job = Job('jobname', example_script)
    job_repr = repr(default_job)
    expected_repr = ('Job(name=jobname, executable=savelist.py, '
                     'universe=vanilla, getenv=True, notification=never)')
    assert job_repr == expected_repr

    job_non_default = Job('jobname', example_script, queue=2)
    job_repr = repr(job_non_default)
    expected_repr = ('Job(name=jobname, executable=savelist.py, '
                     'universe=vanilla, queue=2, getenv=True, '
                     'notification=never)')
    assert job_repr == expected_repr


def test_submit_job_not_built_raises():
    job = Job('jobname', example_script)
    with pytest.raises(ValueError) as excinfo:
        job.submit_job()
    error = 'build() must be called before submit()'
    assert error == str(excinfo.value)


def test_submit_job_parents_raises(tmpdir):
    # Test submitting a Job with parents (not in a Dagman) raises an error
    submit = str(tmpdir)
    job = Job('jobname', example_script, submit=submit)
    parent_job = Job('parent_jobname', example_script)
    job.add_parent(parent_job)
    job.build()
    with pytest.raises(ValueError) as excinfo:
        job.submit_job()
    error = ('Attempting to submit a Job with parents. '
             'Interjob relationships requires Dagman.')
    assert error == str(excinfo.value)


def test_submit_job_children_raises(tmpdir):
    # Test submitting a Job with children (not in a Dagman) raises an error
    submit = str(tmpdir)
    job = Job('jobname', example_script, submit=submit)
    child_job = Job('child_jobname', example_script)
    job.add_child(child_job)
    job.build()
    with pytest.raises(ValueError) as excinfo:
        job.submit_job()
    error = ('Attempting to submit a Job with children. '
             'Interjob relationships requires Dagman.')
    assert error == str(excinfo.value)


def test_add_args_raises():
    # Test that add_args won't accept single argument inputs
    job = Job('jobname', example_script)
    with pytest.raises(TypeError) as excinfo:
        job.add_args('single argument')
    error = 'add_args() is expecting an iterable of argument strings'
    assert error == str(excinfo.value)


def test_add_args():
    # Test that add_args is equivalent to multiple add_arg
    job_1 = Job('job1', example_script)
    for i in range(10):
        job_1.add_arg('file_{}.hdf'.format(i))

    job_2 = Job('job1', example_script)
    job_2.add_args(['file_{}.hdf'.format(i) for i in range(10)])

    assert job_1.args == job_2.args


def test_retry_job_raises():
    # Test that building a Job (not in a Dagman) with a retry raises an error
    job = Job('jobname', example_script)
    job.add_arg('argument', retry=2)
    with pytest.raises(NotImplementedError) as excinfo:
        job.build()
    error = ('Retrying failed Jobs is only available when submitting '
             'from a Dagman.')
    assert error == str(excinfo.value)
