
import pytest
import pycondor


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
