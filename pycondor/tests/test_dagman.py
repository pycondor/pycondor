
import os
import filecmp
import pytest
import pycondor


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
    job_outside_dag = pycondor.Job('job_outside_dag', example_script,
                                   submit=submit_dir, queue=5)
    job_outside_dag.build(fancyname=False)

    # Build Job object that will be built inside of a Dagman
    job_inside_dag = pycondor.Job('job_inside_dag', example_script,
                                  submit=submit_dir, queue=5)
    dagman = pycondor.Dagman('exampledagman', submit=submit_dir)
    dagman.add_job(job_inside_dag)
    dagman.build(fancyname=False)

    # Check that the contents of the two Job submit files are the same
    assert filecmp.cmp(job_outside_dag.submit_file, job_inside_dag.submit_file,
                       shallow=False)
