
import os
import filecmp
import pytest
import pycondor
from .utils import clear_pycondor_environment_variables

clear_pycondor_environment_variables()


def test_add_job_int_fail():
    with pytest.raises(TypeError) as excinfo:
        dag = pycondor.Dagman('dagname')
        dag.add_job(50)
    error = 'Expecting a Job or Dagman. ' + \
            'Got an object of type {}'.format(type(50))
    assert error == str(excinfo.value)


def test_job_dag_submit_file_same(tmpdir):
    # Test to check that the submit file for a Job with no arguments is the
    # same whether built from a Dagman or not. See issue #38.

    example_script = os.path.join('examples/savelist.py')
    submit_dir = str(tmpdir.mkdir('submit'))
    # Build Job object that will be built outside of a Dagman
    job_outside_dag = pycondor.Job('test_job', example_script,
                                   submit=submit_dir, queue=5)
    job_outside_dag.build(fancyname=False)

    # Build Job object that will be built inside of a Dagman
    job_inside_dag = pycondor.Job('test_job', example_script,
                                  submit=submit_dir, queue=5)
    dagman = pycondor.Dagman('exampledagman', submit=submit_dir)
    dagman.add_job(job_inside_dag)
    dagman.build(fancyname=False)

    # Check that the contents of the two Job submit files are the same
    assert filecmp.cmp(job_outside_dag.submit_file, job_inside_dag.submit_file,
                       shallow=False)


def test_job_arg_name_files(tmpdir):
    # Test to check that when a named argument is added to a Job, and the Job
    # is built with fancyname=True, the Job submit file and the
    # error/log/output files for the argument start with the same index.
    # E.g. job_(date)_01.submit, job_(date)_01.error, etc.
    # Regression test for issue #47
    example_script = os.path.join('examples/savelist.py')
    submit_dir = str(tmpdir.mkdir('submit'))

    for fancyname in [True, False]:
        job = pycondor.Job('testjob', example_script, submit=submit_dir)
        job.add_arg('arg', name='argname')
        dagman = pycondor.Dagman('testdagman', submit=submit_dir)
        dagman.add_job(job)
        dagman.build(fancyname=fancyname)

        with open(dagman.submit_file, 'r') as dagman_submit_file:
            dagman_submit_lines = dagman_submit_file.readlines()

        # Get root of the dagman submit file (submit file basename w/o .submit)
        submit_file_line = dagman_submit_lines[0]
        submit_file_basename = submit_file_line.split('/')[-1].rstrip()
        submit_file_root = os.path.splitext(submit_file_basename)[0]
        # Get job_name variable (used to built error/log/output file basenames)
        jobname_line = dagman_submit_lines[2]
        jobname = jobname_line.split('"')[-2]
        other_file_root = '_'.join(jobname.split('_')[:-1])

        assert submit_file_root == other_file_root
