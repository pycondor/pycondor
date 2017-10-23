
import pytest
from datetime import datetime
import subprocess
from pycondor.command_line import line_to_datetime, progress_bar_str


def test_line_to_datetime():
    test_line = '''10/22/17 09:38:40  Done     Pre   Queued    Post   Ready
    Un-Ready   Failed'''
    test_datetime = datetime(17, 10, 22, 9, 38, 40)
    dt = line_to_datetime(test_line)
    assert dt == test_datetime


def test_progress_bar_str_fail():
    with pytest.raises(TypeError) as excinfo:
        progress_bar_str('not-a-status-object', datetime.now(), datetime.now())
    error = 'status must be of type Status'
    assert error == str(excinfo.value)


def test_dagman_progress_fail():
    bad_file = '/path/to/non-existant/submit_file.submit'
    cmd = 'dagman_progress {}'.format(bad_file)
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    err_message = 'IOError: Dagman submit file {} doesn\'t exist'.format(
                                                                    bad_file)
    assert err_message in err
