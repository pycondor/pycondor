
import os
import subprocess
from collections import namedtuple

from . import base

JobArg = namedtuple('JobArg', ['arg', 'name', 'retry'])

class Job(base.SubmitFile):

    def __init__(self, name, executable, error=None, log=None, output=None, submit=os.getcwd(),
    request_memory=None, request_disk=None, request_cpus=None, getenv=True, universe='vanilla',
    initialdir=None, notification='never', requirements=None, queue=None, extra_lines=None,
    verbose=0):

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

    def __len__(self):
        return len(self.args)

    def add_arg(self, arg, name=None, retry=None):
        # Validate user input
        if not isinstance(arg, str):
            raise ValueError('arg must be a string')
        elif name and not isinstance(name, str):
            raise ValueError('name must be a string')
        elif retry and not isinstance(retry, int):
            raise ValueError('retry must be an int')

        job_arg = JobArg(arg=arg, name=name, retry=retry)
        self.args.append(job_arg)
        self.logger.debug('Added argument \'{}\' to Job {}'.format(arg, self.name))

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
        if not isinstance(job, Job):
            raise ValueError('job must be of type Job')

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
        if not isinstance(job, Job):
            raise ValueError('job must be of type Job')

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

        # Retrying failed nodes is only available to Jobs in a Dagman
        self._has_arg_retries = any([job_arg.retry for job_arg in self.args])
        if self._has_arg_retries and (not indag):
            message = 'Retrying failed Jobs is only available when submitting from a Dagman.'
            self.logger.error(message)
            raise NotImplementedError(message)

        # Check that paths/files exist
        if not os.path.exists(self.executable):
            raise IOError('The path {} does not exist...'.format(self.executable))
        for directory in [self.submit, self.log, self.output, self.error]:
            if directory is not None:
                base.checkdir(directory + '/', makedirs)

        name = self._get_fancyname() if fancyname else self.name
        submit_file= '{}/{}.submit'.format(self.submit, name)

        # Start constructing lines to go into job submit file
        lines = []
        submit_attrs = ['universe', 'executable', 'request_memory',
                        'request_disk', 'request_cpus', 'getenv',
                        'initialdir', 'notification', 'requirements']
        for attr in submit_attrs:
            if getattr(self, attr) is not None:
                attr_str = base.string_rep(getattr(self, attr))
                lines.append('{} = {}'.format(attr, attr_str))

        # Set up log, output, and error files paths
        self._has_arg_names = any([arg.name for arg in self.args])
        for attr in ['log', 'output', 'error']:
            if getattr(self, attr) is not None:
                path = getattr(self, attr)
                # If path has trailing '/', then it it removed. Else, path is unmodified
                path = path.rstrip('/')
                if self._has_arg_names:
                    lines.append('{} = {}/$(job_name).{}'.format(attr, path, attr))
                else:
                    lines.append('{} = {}/{}.{}'.format(attr, path, name, attr))

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            lines.extend(self.extra_lines)

        # Add arguments and queue line
        if self.queue is not None and not isinstance(self.queue, int):
            raise ValueError('queue must be of type int')
        # If building this submit file for a job that's being managed by DAGMan, just add simple arguments and queue lines
        if indag:
            lines.append('arguments = $(ARGS)')
            if self._has_arg_names:
                lines.append('job_name = $(job_name)')
            lines.append('queue')
        else:
            if self.args and self.queue:
                if len(self.args) > 1:
                    raise NotImplementedError(
                        'At this time multiple arguments and queue values '
                        'are only supported through Dagman')
                else:
                    arg = self.args[0].arg
                    lines.append('arguments = {}'.format(base.string_rep(arg, quotes=True)))
                    lines.append('queue {}'.format(self.queue))
            # Any arguments supplied will be taken care of via the queue line
            elif self.args:
                for arg, arg_name, _ in self.args:
                    lines.append('arguments = {}'.format(arg))
                    if not self._has_arg_names:
                        pass
                    elif arg_name is not None:
                        lines.append('job_name = {}_{}'.format(name, arg_name))
                    else:
                        lines.append('job_name = {}'.format(name))
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
