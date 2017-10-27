
import os
import subprocess
from collections import namedtuple

from . import utils
from .basenode import BaseNode

JobArg = namedtuple('JobArg', ['arg', 'name', 'retry'])


class Job(BaseNode):
    """Job object

    Parameters
    ----------
    name : str
        Name of the Job instance. This will also be the name of the
        corresponding error, log, output, and submit files associated with
        this job.

    executable : str
        Path to corresponding executable for Job.

    error : str or None, optional
        Path to directory where condor job error files will be written.

    log : str or None, optional
        Path to directory where condor job log files will be written.

    output : str or None, optional
        Path to directory where condor job output files will be written.

    submit : str, optional
        Path to directory where condor job submit files will be written.
        (Defaults to the directory was the job was submitted from).

    request_memory : str or None, optional
        Memory request to be included in submit file.

    request_disk : str or None, optional
        Disk request to be included in submit file.

    request_cpus : int or None, optional
        Number of CPUs to request in submit file.

        .. versionadded:: 0.1.0

    getenv : bool, optional
        Whether or not to use the current environment settings when running
        the job (default is True).

    universe : str, optional
        Universe execution environment to be specified in submit file
        (default is 'vanilla').

    initialdir : str or None, optional
        Initial directory for relative paths (defaults to the directory was
        the job was submitted from).

    notification : str, optional
        E-mail notification preference (default is 'never').

    requirements : str or None, optional
        Additional requirements to be included in ClassAd.

    queue : int or None, optional
        Integer specifying how many times you would like this job to run.

    extra_lines : list or None, optional
        List of additional lines to be added to submit file.

    verbose : int
        Level of logging verbosity option are 0-warning, 1-info,
        2-debugging(default is 0).

    Attributes
    ----------
    args : list
        The list of arguments for this Job instance.

    parents : list
        Only applies when Job is in a Dagman. List of parent Jobs and Dagmans.
        Ensures that Jobs and other Dagmans in the parents list will complete
        before this Job is submitted to HTCondor.

    children : list
        Only applies when Job is in a Dagman. List of child Jobs and Dagmans.
        Ensures that Jobs and other Dagmans in the children list will be
        submitted after this Job is has completed.


    """

    def __init__(self, name, executable, error=None, log=None, output=None,
                 submit=None, request_memory=None, request_disk=None,
                 request_cpus=None, getenv=True, universe='vanilla',
                 initialdir=None, notification='never', requirements=None,
                 queue=None, extra_lines=None, verbose=0):

        super(Job, self).__init__(name, submit, extra_lines, verbose)

        self.executable = utils.string_rep(executable)
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

        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        default_attr = ['name', 'executable', 'logger']
        for attr in vars(self):
            if getattr(self, attr) and attr not in default_attr:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Job(name={}, executable={}{})'.format(
            self.name, os.path.basename(self.executable), nondefaults)
        return output

    def __iter__(self):
        return iter(self.args)

    def __len__(self):
        return len(self.args)

    def add_arg(self, arg, name=None, retry=None):
        """Add argument to Job

        Parameters
        ----------
        arg : str
            Argument to append to Job args list.

        name : str or None, optional
            Option to specify a name related to this argument. If a name is
            specified, then a separate set of log, output, and error files
            will be generated for this particular argument
            (default is ``None``).

            .. versionadded:: 0.1.2

        retry : int or None, optional
            Option to specify the number of times to retry this node. Default
            number of retries is 0. Note: this feature is only available to
            Jobs that are submitted via a Dagman.

            .. versionadded:: 0.1.2

        Returns
        -------
        self : object
            Returns self.

        """
        # Validate user input
        if not isinstance(arg, str):
            raise TypeError('arg must be a string')
        elif name and not isinstance(name, str):
            raise TypeError('name must be a string')
        elif retry and not isinstance(retry, int):
            raise TypeError('retry must be an int')

        job_arg = JobArg(arg=arg, name=name, retry=retry)
        self.args.append(job_arg)
        self.logger.debug('Added argument \'{}\' to Job {}'.format(arg,
                                                                   self.name))

        return self

    def add_args(self, args):
        """Adds multiple arguments to Job

        Parameters
        ----------
        args : list or tuple
            Series of arguments to append to the arguments list

        Returns
        -------
        self : object
            Returns self.

        """
        # Check that args is a list/tuple of str arguments
        if (isinstance(args, (list, tuple)) and
                all([isinstance(arg, str) for arg in args])):
            for arg in args:
                self.add_arg(arg)
        else:
            raise TypeError('add_args() is expecting an iterable of '
                            'argument strings')

        return self

    def _make_submit_script(self, makedirs=True, fancyname=True, indag=False):

        # Retrying failed nodes is only available to Jobs in a Dagman
        self._has_arg_retries = any([job_arg.retry for job_arg in self.args])
        if self._has_arg_retries and (not indag):
            message = 'Retrying failed Jobs is only available when ' + \
                      'submitting from a Dagman.'
            self.logger.error(message)
            raise NotImplementedError(message)

        # Check that paths/files exist
        if not os.path.exists(self.executable):
            raise IOError('The path {} does not exist'.format(self.executable))
        for directory in [self.submit, self.log, self.output, self.error]:
            if directory is not None:
                utils.checkdir(directory + '/', makedirs)

        name = self._get_fancyname() if fancyname else self.name
        submit_file = '{}/{}.submit'.format(self.submit, name)

        # Start constructing lines to go into job submit file
        lines = []
        submit_attrs = ['universe', 'executable', 'request_memory',
                        'request_disk', 'request_cpus', 'getenv',
                        'initialdir', 'notification', 'requirements']
        for attr in submit_attrs:
            if getattr(self, attr) is not None:
                attr_str = utils.string_rep(getattr(self, attr))
                lines.append('{} = {}'.format(attr, attr_str))

        # Set up log, output, and error files paths
        self._has_arg_names = any([arg.name for arg in self.args])
        for attr in ['log', 'output', 'error']:
            if getattr(self, attr) is not None:
                path = getattr(self, attr)
                # If path has trailing '/', then it it removed.
                # Else, path is unmodified
                path = path.rstrip('/')
                if self._has_arg_names:
                    lines.append('{} = {}/$(job_name).{}'.format(
                                 attr, path, attr))
                else:
                    lines.append('{} = {}/{}.{}'.format(attr, path,
                                 name, attr))

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            lines.extend(self.extra_lines)

        # Add arguments and queue line
        if self.queue is not None and not isinstance(self.queue, int):
            raise ValueError('queue must be of type int')
        # If building this submit file for a job that's being managed by DAGMan
        # just add simple arguments and queue lines
        if indag:
            if len(self.args) > 0:
                lines.append('arguments = $(ARGS)')
            if self._has_arg_names:
                lines.append('job_name = $(job_name)')
            if self.queue:
                lines.append('queue {}'.format(self.queue))
            else:
                lines.append('queue')
        else:
            if self.args and self.queue:
                if len(self.args) > 1:
                    raise NotImplementedError(
                        'At this time multiple arguments and queue values '
                        'are only supported through Dagman')
                else:
                    arg = self.args[0].arg
                    lines.append('arguments = {}'.format(utils.string_rep(arg,
                                                         quotes=True)))
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
        self.submit_name = name

        return

    def build(self, makedirs=True, fancyname=True):
        """Build and saves the submit file for Job

        Parameters
        ----------
        makedirs : bool, optional
            If Job directories (e.g. error, output, log, submit) don't exist,
            create them (default is ``True``).

        fancyname : bool, optional
            Appends the date and unique id number to error, log, output, and
            submit files. For example, instead of ``jobname.submit`` the submit
            file becomes ``jobname_YYYYMMD_id``. This is useful when running
            several Jobs of the same name (default is ``True``).

        Returns
        -------
        self : object
            Returns self.

        """
        self.logger.info(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=False)
        self._built = True
        self.logger.info('Condor submission file for {} successfully '
                         'built!'.format(self.name))

        return self

    def _build_from_dag(self, makedirs=True, fancyname=True):
        self.logger.debug(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=True)
        self._built = True
        self.logger.debug('Condor submission file for {} successfully '
                          'built!'.format(self.name))

        return

    def submit_job(self, **kwargs):
        """Submits Job to condor

        Parameters
        ----------
        kwargs : dict, optional
            Any additional options you would like specified when
            ``condor_submit`` is called (see `HTCondor documentation
            <http://research.cs.wisc.edu/htcondor/manual/current/condor_submit.html>`_
            for possible options). For example, if you would like to add
            ``-maxjobs 1000`` to the ``condor_submit`` command, then
            ``kwargs = {'-maxjobs': 1000}``.

        Returns
        -------
        self : object
            Returns self.

        """
        # Ensure that submit file has been written
        if not self._built:
            raise ValueError('build() must be called before submit()')
        # Ensure that there are no parent relationships
        if len(self.parents) != 0:
            raise ValueError('Attempting to submit a Job with the following'
                             ' parents:\n\t{}\nInterjob relationships requires'
                             ' Dagman.'.format(self.parents))
        # Ensure that there are no child relationships
        if len(self.children) != 0:
            raise ValueError('Attempting to submit a Job with the following'
                             ' children:\n\t{}\nInterjob relationships'
                             ' requires Dagman.'.format(self.children))

        if len(self.args) > 20:
            self.logger.warning('You are submitting a Job with {} arguments. '
                                'Consider using a Dagman in the future to '
                                'help monitor jobs.'.format(len(self.args)))

        # Construct and execute condor_submit command
        command = 'condor_submit {}'.format(self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out)

        return

    def build_submit(self, makedirs=True, fancyname=True, **kwargs):
        """Calls build and submit sequentially

        Parameters
        ----------
        makedirs : bool, optional
            If Job directories (e.g. error, output, log, submit) don't exist,
            create them (default is ``True``).

        fancyname : bool, optional
            Appends the date and unique id number to error, log, output, and
            submit files. For example, instead of ``jobname.submit`` the submit
            file becomes ``jobname_YYYYMMD_id``. This is useful when running
            several Jobs of the same name (default is ``True``).

        kwargs : dict, optional
            Any additional options you would like specified when
            ``condor_submit`` is called (see `HTCondor documentation
            <http://research.cs.wisc.edu/htcondor/manual/current/condor_submit.html>`_
            for possible options). For example, if you would like to add
            ``-maxjobs 1000`` to the ``condor_submit`` command, then
            ``kwargs = {'-maxjobs': 1000}``.

        Returns
        -------
        self : object
            Returns self.
        """
        self.build(makedirs, fancyname)
        self.submit_job(**kwargs)

        return
