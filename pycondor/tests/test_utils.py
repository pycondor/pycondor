
import os
import pytest
import pycondor
from pycondor.utils import (clear_pycondor_environment_variables, checkdir,
                            assert_command_exists, get_condor_version)


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


def test_checkdir(tmpdir):
    test_file = str(tmpdir.join('outdir/file.hdf'))
    outdir = os.path.dirname(test_file)

    # Test that when makedirs=False, the proper error is raises
    with pytest.raises(IOError) as excinfo:
        checkdir(test_file, makedirs=False)
    error = 'The directory {} doesn\'t exist'.format(outdir)
    assert error == str(excinfo.value)

    # Test that when makedirs=True, the proper directory is created
    checkdir(test_file, makedirs=True)
    assert os.path.exists(outdir)


def test_checkdir_cwd():
    checkdir('local_file.txt', makedirs=False)


def test_assert_command_exists():
    # Check that ls exists
    assert_command_exists('ls')

    # Check that a non-existant command raises an OSError
    with pytest.raises(OSError) as excinfo:
        cmd = 'not_an_existing_command'
        assert_command_exists(cmd)
    error = 'The command \'{}\' was not found on this machine.'.format(cmd)
    assert error == str(excinfo.value)


@pytest.mark.skipif(os.getenv('CONTINUOUS_INTEGRATION') is None,
                    reason='Travis does not have HTCondor installed')
def test_get_condor_version_raises():
    with pytest.raises(OSError) as excinfo:
        get_condor_version()
    error = 'Could not find HTCondor version.'
    assert error == str(excinfo.value)
