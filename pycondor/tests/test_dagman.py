
import pytest
import pycondor


def test_add_job_int_fail():
    with pytest.raises(TypeError) as excinfo:
        dag = pycondor.Dagman('dagname')
        dag.add_job(50)
    error = 'Expecting a Job or Dagman. ' + \
            'Got an object of type {}'.format(type(50))
    assert error == str(excinfo.value)
