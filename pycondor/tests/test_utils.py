
import os
import pytest
import pycondor
from pycondor.utils import clear_pycondor_environment_variables


def test_string_rep_None_fail():
    with pytest.raises(AssertionError) as excinfo:
        pycondor.utils.string_rep(None)
    error = 'Input must not be None'
    assert error == str(excinfo.value)


def test_string_rep_list():
    assert pycondor.utils.string_rep([1, 2, 3]) == '1, 2, 3'


def test_string_rep_list_quotes():
    assert pycondor.utils.string_rep([1, 2, 3], quotes=True) == '"1, 2, 3"'


def test_setup_logger_noname_fail():
    with pytest.raises(AttributeError) as excinfo:
        pycondor.utils._setup_logger('string_has_no_name')
    error = 'Input must have a "name" attribute.'
    assert error == str(excinfo.value)


def test_clear_pycondor_environment_variables():
    # Test that environment variables are cleared
    clear_pycondor_environment_variables()
    for i in ['submit', 'output', 'error', 'log']:
        assert os.environ['PYCONDOR_{}_DIR'.format(i.upper())] == ''
