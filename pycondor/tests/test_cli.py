
import pytest
import os
from datetime import datetime
import subprocess
from click.testing import CliRunner

import pycondor
from pycondor.cli import (line_to_datetime, progress_bar_str, Status, _states,
                          status_generator, monitor, submit)

pycondor_dir = os.path.dirname(pycondor.__file__)
example_dagman_submit = os.path.join(pycondor_dir,
                                     'tests',
                                     'test_dagman.submit')


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


def test_progress_bar_str():
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


def test_progress_bar_str_null_status():
    # Test that a null status (all zeroes) is handled properly
    jobs = [0]*len(_states)
    status = Status(*jobs)
    prog_bar_str = progress_bar_str(status, datetime.now(), datetime.now(),
                                    length=30, prog_char='#')

    test_str = ('\r[                              ] 0% Done | 0 done, '
                '0 queued, 0 ready, 0 unready, 0 failed | 0.0m')
    assert prog_bar_str == test_str


def test_status_generator():
    dag_out_file = os.path.join(pycondor_dir,
                                'tests',
                                'exampledagman.submit.dagman.out')

    status_gen = status_generator(dag_out_file)
    status, datetime_current = next(status_gen)

    test_status = Status(Done=2, Pre=0, Queued=1, Post=0, Ready=0,
                         UnReady=0, Failed=0)
    test_datetime = datetime(17, 11, 22, 11, 17, 59)

    assert status == test_status
    assert datetime_current == test_datetime


def test_monitor_pass():
    runner = CliRunner()
    result = runner.invoke(monitor, [example_dagman_submit])
    assert result.exit_code == 0
    expected_output = ('\r[##############################] 100% Done | '
                       '3 done, 0 queued, 0 ready, 0 unready, 0 failed | 1.2m')
    assert result.output == expected_output


def test_monitor_file_raises():
    non_exist_file = 'file.submit'

    runner = CliRunner()
    result = runner.invoke(monitor, [non_exist_file])
    assert result.exit_code == 2
    expected_output = ('Usage: monitor [OPTIONS] FILE\n\nError: Invalid '
                       'value for "file": Path "{}" does not '
                       'exist.\n'.format(non_exist_file))
    assert result.output.replace('\r', '') == expected_output


def test_dagman_progress_deprecation_message():
    command = 'dagman_progress {}'.format(example_dagman_submit)
    proc = subprocess.Popen([command],
                            stderr=subprocess.PIPE,
                            shell=True)
    _, err = proc.communicate()

    deprecation_message = ('DeprecationWarning: The dagman_progress command '
                           'is now depreciated and will be removed in version '
                           '0.2.2. Please use the new "pycondor monitor" '
                           'command instead.')

    assert deprecation_message in err


def test_submit_file_raises():
    non_exist_executable = '/this/does/not/exist.py'

    runner = CliRunner()
    result = runner.invoke(submit, [non_exist_executable])
    assert result.exit_code == 2
    expected_output = ('Usage: submit [OPTIONS] EXECUTABLE [ARGS]'
                       '...\n\nError: Invalid value for "executable": Path '
                       '"{}" does not exist.\n'.format(non_exist_executable))
    assert result.output.replace('\r', '') == expected_output
