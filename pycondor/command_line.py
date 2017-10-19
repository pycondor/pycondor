
from __future__ import division, print_function
import os
import sys
import time
from collections import deque, namedtuple
import argparse


Status = namedtuple('Status', ['Done', 'Pre', 'Queued', 'Post', 'Ready',
                               'UnReady', 'Failed'])


class NoStatusLineFound(Exception):
    '''
    Raised when no lines containing the dagman job status are found
    '''
    pass


def get_status(dag_out_file, n_lines=100):
    '''Function to parse dag_out_file

    Parses the last n_lines lines of dag_out_file (from bottom to top)
    and searches for a line containing the current status of the dagman.

    Parameters
    ----------
    dag_out_file : str
        Path to dagman out file to parse.
    n_lines : int, optional
        Number of lines to parse at the end of dag_out_file (default is 100).

    Returns
    -------
    status : Status
        Status namedtuple that contains the current number of jobs that are
        done, queued, ready, failed, etc.

    Raises
    ------
    NoStatusLineFound
        If no line containing the dagman job status is found.
    '''
    # Read in last n_lines lines of dag_out_file
    tail = deque(open(dag_out_file, 'r'), n_lines)
    lines = list(reversed(tail))
    node_counts = []
    for idx, line in enumerate(lines):
        if 'Done     Pre   Queued    Post   Ready   Un-Ready   Failed' in line:
            num_line = lines[idx-2]
            node_counts = [i for i in num_line.split(' ')
                           if i != '' and ':' not in i and '/' not in i]
            node_counts = map(int, node_counts)
            break

    if node_counts:
        status = Status(*node_counts)
        return status
    else:
        raise NoStatusLineFound('No line with number of jobs found yet')


def progress_bar_str(status, length=30, prog_char='#'):
    '''Function to convert a Status object into a progress string

    Parameters
    ----------
    status : Status
        Status namedtuple that contains the current number of jobs that are
        done, queued, ready, failed, etc.
    length : int, optional
        Width of the progress bar (default is 30).
    prog_char : str, optional
        Character used to fill the progress bar (default is '#').

    Returns
    -------
    prog_bar_str : str
        Progress bar string.
    '''
    n_total = sum(status)
    n_done = status.Done
    frac_done = n_done / n_total
    width = int(frac_done * length)

    bar_str = '\r[{0:<{1}}] | {2:0.0%} complete'.format(prog_char*width,
                                                        length,
                                                        frac_done)
    count_str = '({} done, {} queued, {} ready, {} unready, {} failed)'.format(
            status.Done, status.Queued, status.Ready,
            status.UnReady, status.Failed)
    prog_bar_str = bar_str + ' ' + count_str
    return prog_bar_str


def dagman_progress():
    '''Function to print Dagman progress bar to stdout
    '''

    parser = argparse.ArgumentParser(description='Prints dagman progress bar')
    parser.add_argument('file', help='Dagman submit file')
    parser.add_argument('-t', '--time', dest='time', default=10, type=float,
                        help='Time (in seconds) in between log checks')
    parser.add_argument('--n_lines', dest='n_lines', default=100, type=int,
                        help='Number of lines to parse')
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

    while True:
        try:
            status = get_status(dag_out_file, n_lines=args.n_lines)
            prog_str = progress_bar_str(status, length=args.length,
                                        prog_char=args.prog_char)
            sys.stdout.write(prog_str)
            sys.stdout.flush()
            # If all jobs are either Done or Failed, exit
            if status.Done + status.Failed == sum(status):
                sys.exit()
            time.sleep(args.time)
        except NoStatusLineFound:
            time.sleep(args.time)
            pass
        except KeyboardInterrupt:
            print('\nExiting dagman_progress...')
            sys.exit()
