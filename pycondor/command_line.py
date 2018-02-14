
from __future__ import division, print_function
import os
import sys
import time
from collections import namedtuple
import argparse
from datetime import datetime
from .job import Job

_states = ['Done', 'Pre', 'Queued', 'Post', 'Ready', 'UnReady', 'Failed']
Status = namedtuple('Status', _states)


def line_to_datetime(line):
    '''Function to extract a datetime from a dagman out file line

    Parameters
    ----------
    line : str
        Any line from a .dagman.out file.

    Returns
    -------
    dt : datetime.datetime
        Datetime stamp from line in out file.
    '''
    date_str = line.split(' ')[0]
    time_str = line.split(' ')[1]
    month, day, year = map(int, date_str.split('/'))
    hour, minute, second = map(int, time_str.split(':'))
    dt = datetime(year, month, day, hour, minute, second)

    return dt


def status_generator(dag_out_file):
    '''Generator to yield dagman status

    Parameters
    ----------
    dag_out_file : str
        Path to dagman out file to parse.

    Returns
    -------
    status : Status
        Status namedtuple that contains the current number of jobs that are
        done, queued, ready, failed, etc. If no line is found indicating the
        current dagman status, an empty Status object is returned.
    datetime_current : datetime.datetime
        Current datetime. If
    '''
    status_str = 'Done     Pre   Queued    Post   Ready   Un-Ready   Failed'
    with open(dag_out_file, 'r') as file_object:
        while True:
            lines = file_object.readlines()
            node_counts = []
            datetime_current = None
            # Reverse order of lines to get most recent status of the dagman
            lines = lines[::-1]
            for idx, line in enumerate(lines):
                if idx == 0:
                    datetime_current = line_to_datetime(line)
                if status_str in line:
                    num_line = lines[idx-2]
                    node_counts = [i for i in num_line.split(' ') if i != ''
                                   and ':' not in i and '/' not in i]
                    node_counts = map(int, node_counts)
                    break

            if node_counts:
                status = Status(*node_counts)
            else:
                status = Status(*[0]*len(_states))
                datetime_current = datetime.now()

            yield status, datetime_current


def progress_bar_str(status, datetime_start, datetime_current, length=30,
                     prog_char='#'):
    '''Function to convert a Status object into a progress bar string

    Parameters
    ----------
    status : Status
        Status namedtuple that contains the current number of jobs that are
        done, queued, ready, failed, etc.
    datetime_start : datetime.datetime
        Datetime for the first line of the dagman out file.
    datetime_current : datetime.datetime
        Datetime for the current line of the dagman out file.
    length : int, optional
        Width of the progress bar (default is 30).
    prog_char : str, optional
        Character used to fill the progress bar (default is '#').

    Returns
    -------
    prog_bar_str : str
        Progress bar string.
    '''
    if not isinstance(status, Status):
        raise TypeError('status must be of type Status')
    n_total = sum(status)
    n_done = status.Done
    try:
        frac_done = n_done / n_total
    except ZeroDivisionError:
        frac_done = 0
    width = int(frac_done * length)

    bar_str = '\r[{0:<{1}}] {2}% Done'.format(prog_char*width, length,
                                              int(100*frac_done))
    count_str = '{} done, {} queued, {} ready, {} unready, {} failed'.format(
            status.Done, status.Queued, status.Ready,
            status.UnReady, status.Failed)

    dt = datetime_current - datetime_start
    time_str = '{:0.1f}m'.format(dt.seconds / 60)

    prog_bar_str = ' | '.join([bar_str, count_str, time_str])

    return prog_bar_str


def dagman_progress():
    '''Function to print Dagman progress bar to stdout
    '''
    parser = argparse.ArgumentParser(description='Prints dagman progress bar')
    parser.add_argument('file', help='Dagman submit file')
    parser.add_argument('-t', '--time', dest='time', default=30, type=float,
                        help='Time (in seconds) in between log checks')
    parser.add_argument('-l', '--length', dest='length', default=30, type=int,
                        help='Length of the progress bar')
    parser.add_argument('--prog_char', dest='prog_char', default='#',
                        help='Progress bar character')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise IOError('Dagman submit file {} doesn\'t exist'.format(args.file))

    dag_out_file = args.file + '.dagman.out'
    # Make sure dagman out file exists
    # It isn't created until the dagman beings running
    while not os.path.exists(dag_out_file):
        sys.stdout.write(
            '\rWaiting for dagman {} to begin running...'.format(args.file))
        sys.stdout.flush()
        time.sleep(args.time)

    datetime_start = line_to_datetime(open(dag_out_file, 'r').readline())
    current_status = Status(*[0]*len(_states))
    try:
        for status, datetime_current in status_generator(dag_out_file):
            # If no line with dagman status is found, wait and try again
            if sum(status) != 0:
                current_status = status

            prog_str = progress_bar_str(current_status,
                                        datetime_start=datetime_start,
                                        datetime_current=datetime_current,
                                        length=args.length,
                                        prog_char=args.prog_char)
            sys.stdout.write(prog_str)
            sys.stdout.flush()
            # Exit if all jobs are either Done or Failed
            n_finished = current_status.Done + current_status.Failed
            if n_finished == sum(current_status) and sum(current_status) != 0:
                sys.exit()
            else:
                time.sleep(args.time)
    except KeyboardInterrupt:
        print('\nExiting dagman_progress...')
        sys.exit()


def pycondor_submit():
    '''Function to quickly submit a Job from the command line
    '''
    parser = argparse.ArgumentParser(description='Submits executable to HTCondor')
    parser.add_argument('command')
    parser.add_argument('--submit', dest='submit',
                        help='Directory to store submit files')
    parser.add_argument('--log', dest='log',
                        help='Directory to store log files')
    parser.add_argument('--output', dest='output',
                        help='Directory to store output files')
    parser.add_argument('--error', dest='error',
                        help='Directory to store error files')
    parser.add_argument('--request_memory', dest='request_memory',
                        help='Memory request to be included in submit file')
    parser.add_argument('--request_disk', dest='request_disk',
                        help='Disk request to be included in submit file')
    parser.add_argument('--request_cpus', dest='request_cpus',
                        help='Number of CPUs to request in submit file')
    parser.add_argument('--universe', dest='universe',
                        default='vanilla',
                        help=('Universe execution environment to be specified '
                              'in submit file (default is \'vanilla\')'))
    parser.add_argument('--no-getenv', dest='no_getenv',
                        action='store_true',
                        default=False,
                        help='Set getenv equal to False')
    args = parser.parse_args()

    if ' ' not in args.command:
        executable = args.command
        arguments = None
    else:
        executable = args.command.split(' ')[0]
        arguments = args.command.replace(executable + ' ', '')

    basename = os.path.basename(executable)
    name, _ = os.path.splitext(basename)

    job = Job(name=name,
              executable=executable,
              submit=args.submit,
              log=args.log,
              output=args.output,
              error=args.error,
              request_memory=args.request_memory,
              request_disk=args.request_disk,
              request_cpus=args.request_cpus,
              universe=args.universe,
              getenv=not args.no_getenv,
              )
    if arguments is not None:
        job.add_arg(arguments)
    job.build_submit()
