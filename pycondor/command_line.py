
from __future__ import division, print_function
import os
import sys
import time
from collections import deque, namedtuple
import argparse


Status = namedtuple('Status', ['Done', 'Pre', 'Queued', 'Post', 'Ready',
                               'UnReady', 'Failed'])


class EarlyInLogFile(Exception):
    '''
    Raised when a .dagman.out exists, but no line with the number of done jobs
    has been written to the file yet.
    '''
    pass


def get_status(lines):
    values = []
    for idx, line in enumerate(lines):
        if 'Done     Pre   Queued    Post   Ready   Un-Ready   Failed' in line:
            num_line = lines[idx-2]
            values = [i for i in num_line.split(' ')
                      if i != '' and ':' not in i and '/' not in i]
            values = [i.rstrip() for i in values]
            values = map(int, values)
            break

    if values:
        status = Status(*values)
        return status
    else:
        raise EarlyInLogFile('No line with number of jobs found yet')


def progress_bar_str(status, length=30):
    n_total = sum(status)
    n_done = status.Done
    frac_done = n_done / n_total
    width = int(frac_done * length)

    prog_str = '\r[{0:<{1}}] | {2:0.0%} complete'.format('#'*width, length,
                                                         frac_done)
    count_str = '({} done, {} queued, {} ready, {} unready, {} failed)'.format(
            status.Done, status.Queued, status.Ready,
            status.UnReady, status.Failed)
    return prog_str + ' ' + count_str


def dagman_progress():

    parser = argparse.ArgumentParser(description='Prints dagman progress bar')
    parser.add_argument('file', help='Dagman submit file')
    parser.add_argument('-t', '--time', dest='time', default=10, type=float,
                        help='Time (in seconds) in between log checks')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise IOError('Dagman submit file {} doesn\'t exist'.format(args.file))

    dag_out_file = args.file + '.dagman.out'
    # Make sure dagman out file exists
    while not os.path.exists(dag_out_file):
        sys.stdout.write(
            '\rWaiting for dagman {} to begin running...'.format(args.file))
        sys.stdout.flush()
        time.sleep(args.time)

    while True:
        try:
            tail = deque(open(dag_out_file, 'r'), 50)
            status = get_status([tail[idx] for idx in
                                 reversed(range(len(tail)))])
            prog_str = progress_bar_str(status)
            sys.stdout.write(prog_str)
            sys.stdout.flush()
            time.sleep(args.time)

            if status.Done == sum(status):
                sys.exit()
        except EarlyInLogFile:
            time.sleep(args.time)
            pass
        except KeyboardInterrupt:
            print('Exiting monitor_dag ...')
            sys.exit()
