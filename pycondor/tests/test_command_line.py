
import pytest
from datetime import datetime
from pycondor.command_line import (line_to_datetime, progress_bar_str,
                                   Status, _states)


def test_line_to_datetime():
    test_line = '''10/22/17 09:38:40  Done     Pre   Queued    Post   Ready
    Un-Ready   Failed'''
    test_datetime = datetime(17, 10, 22, 9, 38, 40)
    dt = line_to_datetime(test_line)
    assert dt == test_datetime


def test_progress_bar_str_type_fail():
    with pytest.raises(TypeError) as excinfo:
        progress_bar_str('not-a-status-object', datetime.now(), datetime.now())
    error = 'status must be of type Status'
    assert error == str(excinfo.value)


def test_progress_bar():
    # Test to check the output of progress_bar_str

    # Create status that is 99.5% done. Want to make sure this is displayed
    # as 99% done, not 100% done. See issue #51.
    jobs = [0]*len(_states)
    jobs[0], jobs[2] = 199, 1
    status = Status(*jobs)
    prog_bar_str = progress_bar_str(status, datetime.now(), datetime.now(),
                                    length=30, prog_char='#')

    test_str = '\r[############################# ] 99% Done | 199 done, ' + \
               '1 queued, 0 ready, 0 unready, 0 failed | 0.0m'
    assert prog_bar_str == test_str
