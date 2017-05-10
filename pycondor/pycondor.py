
import os
import glob
import time
import subprocess

from . import base
from . import logger


class BaseSubmitNode(object):

    def __init__(self, name, submit=os.getcwd(), extra_lines=None, verbose=0):

        self.name = base.string_rep(name)
        self.submit = submit
        self.extra_lines = extra_lines
        self._built = False
        # Set up logger
        self.logger = logger._setup_logger(self, verbose)

    def _get_fancyname(self):
        date = time.strftime('%Y%m%d')
        othersubmits = glob.glob('{}/{}_{}_??.submit'.format(self.submit,
                                                             self.name, date))
        submit_number = len(othersubmits) + 1
        fancyname = self.name + \
            '_{}'.format(date) + '_{:02d}'.format(submit_number)
        return fancyname


class Job(BaseSubmitNode):

    def __init__(self, name, executable, error=None, log=None, output=None, submit=os.getcwd(),
    request_memory=None, request_disk=None, request_cpus=None, getenv=True, universe='vanilla',
    initialdir=None, notification='never', requirements=None, queue=None, extra_lines=None,
    use_unique_id=False, verbose=0):

        super(Job, self).__init__(name, submit, extra_lines, verbose)

        self.executable = base.string_rep(executable)
        self.error = error
        self.log = log
        self.output = output
        self.request_memory = request_memory
        self.request_disk = request_disk
        self.request_cpus = request_cpus
        self.getenv = getenv
        self.universe = universe
        self.initialdir = initialdir
        self.notification = notification
        self.requirements = requirements
        self.queue = queue
        self.use_unique_id = use_unique_id

        self.args = []
        self.parents = []
        self.children = []

        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'executable', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Job(name={}, executable={}{})'.format(self.name, os.path.basename(self.executable), nondefaults)
        return output

    def __iter__(self):
        return iter(self.args)

    def add_arg(self, arg):
        arg_str = base.string_rep(arg)
        self.args.append(arg_str)
        self.logger.debug(
            'Added argument \'{}\' to Job {}'.format(arg_str, self.name))

        return self

    def add_args(self, args):
        try:
            for arg in args:
                self.add_arg(arg)
        except:
            raise TypeError(
                'add_args() is expecting an iterable of argument strings')

        return self

    def _hasparent(self, job):
        return job in self.parents

    def add_parent(self, job):

        # Ensure that job is a Job
        assert isinstance(job, Job), 'job must be of type Job'

        # Don't bother continuing if job is already in the parents list
        if self._hasparent(job):
            return self

        # Add job to existing parents
        self.parents.append(job)
        self.logger.debug(
            'Added Job {} as a parent for Job {}'.format(job.name, self.name))

        # Add self Job instance as a child to the new parent job
        job.add_child(self)

        return self

    def add_parents(self, job_list):

        # Ensure that job_list is an iterable of type Job
        try:
            for job in job_list:
                self.add_parent(job)
        except:
            raise TypeError('add_parents() is expecting an iterable of Jobs')

        return self

    def _haschild(self, job):
        return job in self.children

    def add_child(self, job):

        # Ensure that job is a Job
        assert isinstance(job, Job), 'job must be of type Job'

        # Don't bother continuing if job is already in the children list
        if self._haschild(job):
            return self

        # Add job to existing children
        self.children.append(job)
        self.logger.debug(
            'Added Job {} as a child for Job {}'.format(job.name, self.name))
        # Add this Job instance as a parent to the new child job
        job.add_parent(self)

        return self

    def add_children(self, jobs):

        # Ensure that jobs is an iterable of type Job
        try:
            for job in jobs:
                self.add_child(job)
        except:
            raise TypeError('add_children() is expecting a list of Jobs')

        return self

    def haschildren(self):
        return bool(self.children)

    def hasparents(self):
        return bool(self.parents)

    def _make_submit_script(self, makedirs=True, fancyname=True, indag=False):


        # Check that paths/files exist
        if not os.path.exists(self.executable):
            raise IOError(
                'The path {} does not exist...'.format(self.executable))
        for directory in [self.submit, self.log, self.output, self.error]:
            if directory is not None:
                base.checkdir(directory + '/', makedirs)

        name = self._get_fancyname() if fancyname else self.name
        submit_file= '{}/{}.submit'.format(self.submit, name)

        # Start constructing lines to go into job submit file
        lines = []
        submit_attrs = ['universe', 'executable', 'request_memory', 'request_disk', 'request_cpus', 'getenv', 'initialdir', 'notification', 'requirements']
        for attr in submit_attrs:
            if getattr(self, attr) is not None:
                attr_str = base.string_rep(getattr(self, attr))
                lines.append('{} = {}'.format(attr, attr_str))

        # Set up files paths
        for attr in ['log', 'output', 'error']:
            if getattr(self, attr) is not None:
                path = getattr(self, attr)
                # If path has trailing '/', then it it removed. Else, path is unmodified
                path = path.rstrip('/')
                if getattr(self, 'use_unique_id'):
                    lines.append('{} = {}/{}_$(Cluster).$(Process).{}'.format(attr, path, name, attr))
                else:
                    lines.append('{} = {}/{}.{}'.format(attr, path, name, attr))

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            extra_lines = self.extra_lines
            assert isinstance(extra_lines, (str, list, tuple)), 'extra_lines must be of type str, list, or tuple'
            if isinstance(extra_lines, str):
                lines.append(extra_lines)
            else:
                lines.extend(extra_lines)

        # Add arguments and queue line
        if self.queue:
            assert isinstance(self.queue, int), 'queue must be of type int'
        # If building this submit file for a job that's being managed by DAGMan, just add simple arguments and queue lines
        if indag:
            lines.append('arguments = $(ARGS)')
            lines.append('queue')
        else:
            if self.args and self.queue:
                if len(self.args) > 1:
                    message = 'At this time multiple arguments and queue values are only supported through Dagman'
                    self.logger.error(message)
                    raise NotImplementedError(message)
                else:
                    lines.append('arguments = {}'.format(base.string_rep(self.args, quotes=True)))
                    lines.append('queue {}'.format(self.queue))
            # Any arguments supplied will be taken care of via the queue line
            elif self.args:
                for arg in self.args:
                    lines.append('arguments = {}'.format(base.string_rep(arg)))
                    lines.append('queue')
            elif self.queue:
                lines.append('queue {}'.format(self.queue))
            else:
                lines.append('queue')

        with open(submit_file, 'w') as f:
            f.writelines('\n'.join(lines))

        # Add submit_file data member to job for later use
        self.submit_file = submit_file

        return

    def build(self, makedirs=True, fancyname=True):
        self.logger.info(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=False)
        self._built = True
        self.logger.info('Condor submission file for {} successfully built!'.format(self.name))

        return self

    def _build_from_dag(self, makedirs=True, fancyname=True):
        self.logger.debug(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=True)
        self._built = True
        self.logger.debug('Condor submission file for {} successfully built!'.format(self.name))

        return

    def submit_job(self, **kwargs):
        # Ensure that submit file has been written
        assert self._built, 'build() must be called before submit()'
        # Ensure that there are no parent relationships
        assert len(self.parents) == 0, 'Attempting to submit a Job with the following parents:\n\t{}\nInterjob relationships requires Dagman.'.format(self.parents)
        command = 'condor_submit {}'.format(self.submit_file)
        # Ensure that there are no child relationships
        assert len(self.children) == 0, 'Attempting to submit a Job with the following children:\n\t{}\nInterjob relationships requires Dagman.'.format(self.children)

        if len(self.args) > 20:
            message = 'You are submitting a Job with {} arguments. Consider using a Dagman in the future to help monitor jobs.'.format(len(self.args))
            self.logger.warning(message)

        # Construct and execute condor_submit command
        command = 'condor_submit {}'.format(self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out)

        return

    def build_submit(self, makedirs=True, fancyname=True, **kwargs):
        self.build(makedirs, fancyname)
        self.submit_job(**kwargs)

        return


class Dagman(BaseSubmitNode):

    def __init__(self, name, submit=None, extra_lines=None, verbose=0):

        super(Dagman, self).__init__(name, submit, extra_lines, verbose)

        self.jobs = []
        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'jobs', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Dagman(name={}, n_jobs={}{})'.format(self.name, len(self.jobs), nondefaults)

        return output

    def __iter__(self):
        return iter(self.jobs)

    def _hasjob(self, job):
        return job in self.jobs

    def add_job(self, job):
        # Don't bother adding job if it's already in the jobs list
        if self._hasjob(job):
            return self
        if isinstance(job, Job):
            self.jobs.append(job)
        else:
            raise TypeError('add_job() is expecting a Job')
        self.logger.debug(
            'Added Job {} Dagman {}'.format(job.name, self.name))

        return self

    def build(self, makedirs=True, fancyname=True):
        for job in self.jobs:
            job._build_from_dag(makedirs, fancyname)

        # Create DAG submit file path
        name = self._get_fancyname() if fancyname else self.name
        submit_file = '{}/{}.submit'.format(self.submit, name)
        self.submit_file = submit_file

        # Write dag submit file
        self.logger.info(
            'Building DAG submission file {}...'.format(self.submit_file))
        with open(submit_file, 'w') as dag:
            for job_index, job in enumerate(self, start=1):
                self.logger.info('Working on Job {} [{} of {}]'.format(
                    job.name, job_index, len(self.jobs)))
                for i, arg in enumerate(job):
                    dag.write('JOB {}_part{} '.format(job.name, i) + job.submit_file + '\n')
                    dag.write('VARS {}_part{} '.format(job.name, i) +
                              'ARGS={}\n'.format(base.string_rep(arg, quotes=True)))
                # Add parent/child information if necessary
                if job.hasparents():
                    parent_string = 'Parent'
                    for parentjob in job.parents:
                        for j, parentarg in enumerate(parentjob):
                            parent_string += ' {}_part{}'.format(parentjob.name, j)
                    child_string = 'Child'
                    for k, arg in enumerate(job):
                        child_string += ' {}_part{}'.format(job.name, k)
                    dag.write(parent_string + ' ' + child_string + '\n')

            # Add any extra lines to submit file, if specified
            if self.extra_lines:
                extra_lines = self.extra_lines
                assert isinstance(extra_lines, (str, list, tuple)), 'extra_lines must be of type str, list, or tuple'
                if isinstance(extra_lines, str):
                    extra_lines = [extra_lines]
                for line in extra_lines:
                    dag.write(line + '\n')

        self._built = True
        self.logger.info('DAGMan submission file for {} successfully built!'.format(self.name))

        return self

    def submit_dag(self, maxjobs=3000, **kwargs):
        # Construct and execute condor_submit_dag command
        command = 'condor_submit_dag -maxjobs {} {}'.format(
            maxjobs, self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out)

        return

    def build_submit(self, makedirs=True, fancyname=True, maxjobs=3000, **kwargs):
        self.build(makedirs, fancyname)
        self.submit_dag(maxjobs, **kwargs)

        return
