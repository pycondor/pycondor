
import pytest
import pycondor


def test_add_job_int_fail():
    with pytest.raises(TypeError) as excinfo:
        dag = pycondor.Dagman('dagname')
        dag.add_job(50)
    error = 'add_job() is expecting a Job'
    assert error == str(excinfo.value)
