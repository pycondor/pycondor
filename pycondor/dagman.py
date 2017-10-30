
import os
import subprocess

from . import utils
from .basenode import BaseNode
from .job import Job


def _get_subdag_string(dagman):

    if not isinstance(dagman, Dagman):
        raise TypeError(
                'Expecting a Dagman object, got {}'.format(type(dagman)))

    subdag_string = 'SUBDAG EXTERNAL {} {}'.format(dagman.name,
                                                   dagman.submit_file)

    return subdag_string


def _get_job_arg_lines(job, fancyname):

    if not isinstance(job, Job):
        raise TypeError('Expecting a Job object, got {}'.format(type(job)))
    if not job._built:
        raise ValueError('Job {} must be built before adding it '
                         'to a Dagman'.format(job.name))

    job_arg_lines = []
    if len(job) == 0:
        job_arg_lines.append('JOB {} '.format(job.name) + job.submit_file)
    else:
        for idx, job_arg in enumerate(job):
            arg, name, retry = job_arg
            job_arg_lines.append('JOB {}_arg_{} {}'.format(job.name, idx,
                                 job.submit_file))
            job_arg_lines.append('VARS {}_arg_{} ARGS={}'.format(job.name, idx,
                                 utils.string_rep(arg, quotes=True)))
            # Define job_name variable if there are arg_names present for job
            if not job._has_arg_names:
                pass
            elif name is not None:
                job_name = job.submit_name
                job_name += '_{}'.format(name)
                job_name = utils.string_rep(job_name, quotes=True)
                job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(
                    job.name, idx, job_name))
            else:
                job_name = job.submit_name
                job_name = utils.string_rep(job_name, quotes=True)
                job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(
                    job.name, idx, job_name))
            # Add retry option for Job
            if retry is not None:
                job_arg_lines.append('Retry {}_arg_{} {}'.format(job.name, idx,
                                                                 retry))

    return job_arg_lines


def _get_parent_child_string(node):

    if not isinstance(node, BaseNode):
        raise ValueError('Expecting a Job or Dagman object, '
                         'got {}'.format(type(node)))

    parent_string = 'Parent'
    for parent_node in node.parents:
        if isinstance(parent_node, Job) and len(parent_node) > 0:
            for parent_arg_idx in range(len(parent_node)):
                parent_string += ' {}_arg_{}'.format(parent_node.name,
                                                     parent_arg_idx)
        else:
            parent_string += ' {}'.format(parent_node.name)

    child_string = 'Child'
    if isinstance(node, Job) and len(node) > 0:
        for node_arg_idx in range(len(node)):
            child_string += ' {}_arg_{}'.format(node.name, node_arg_idx)
    else:
        child_string += ' {}'.format(node.name)

    parent_child_string = parent_string + ' ' + child_string

    return parent_child_string


class Dagman(BaseNode):
    """
    Dagman object consisting of a series of Jobs and sub-Dagmans to manage.

    Note that the ``submit`` parameter can be explicitly given or configured
    by setting the ``PYCONDOR_SUBMIT_DIR`` environment variable. An explicitly
    given value for ``submit`` will be used over the environment variable,
    while the environment variable will be used over a default value.

    Parameters
    ----------
    name : str
        Name of the Dagman instance. This will also be the name of the
        corresponding error, log, output, and submit files associated with
        this Dagman.

    submit : str
        Path to directory where condor dagman submit files will be written
        (defaults to the directory was the Dagman was submitted from).

    extra_lines : list or None, optional
        List of additional lines to be added to submit file.

        .. versionadded:: 0.1.1

    verbose : int, optional
        Level of logging verbosity option are 0-warning, 1-info,
        2-debugging (default is 0).

    Attributes
    ----------
    jobs : list
        The list of jobs for this Dagman instance to manage.

    parents : list
        List of parent Jobs and Dagmans. Ensures that Jobs and Dagmans in the
        parents list will complete before this Dagman is submitted to HTCondor.

    children : list
        List of child Jobs and Dagmans. Ensures that Jobs and Dagmans in the
        children list will be submitted only after this Dagman has completed.

    """

    def __init__(self, name, submit=None, extra_lines=None, verbose=0):

        super(Dagman, self).__init__(name, submit, extra_lines, verbose)

        self.nodes = []
        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'nodes', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Dagman(name={}, n_nodes={}{})'.format(self.name,
                                                        len(self.nodes),
                                                        nondefaults)

        return output

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def _hasnode(self, node):
        return node in self.nodes

    def _add_node(self, node):
        # Don't bother adding node if it's already been added
        if self._hasnode(node):
            return self
        if isinstance(node, BaseNode):
            self.nodes.append(node)
        else:
            raise TypeError('Expecting a Job or Dagman. '
                            'Got an object of type {}'.format(type(node)))
        self.logger.debug(
            'Added {} to Dagman {}'.format(node.name, self.name))

        return self

    def add_job(self, job):
        """Add job to Dagman

        Parameters
        ----------
        job : Job
            Job to append to Dagman jobs list.


        Returns
        -------
        self : object
            Returns self.

        """
        self._add_node(job)

        return self

    def add_subdag(self, dag):
        """Add dag to Dagman

        Parameters
        ----------
        dag : Dagman
            Subdag to append to Dagman jobs list.


        Returns
        -------
        self : object
            Returns self.

        """
        self._add_node(dag)

        return self

    def build(self, makedirs=True, fancyname=True):
        """Build and saves the submit file for Dagman

        Parameters
        ----------
        makedirs : bool, optional
            If Job directories (e.g. error, output, log, submit) don't exist,
            create them (default is ``True``).

        fancyname : bool, optional
            Appends the date and unique id number to error, log, output, and
            submit files. For example, instead of ``dagname.submit`` the submit
            file becomes ``dagname_YYYYMMD_id``. This is useful when running
            several Dags/Jobs of the same name (default is ``True``).

        Returns
        -------
        self : object
            Returns self.
        """

        if self._built:
            self.logger.warning(
                    '{} submit file has already been built. '
                    'Skipping the build process...'.format(self.name))
            return self

        name = self._get_fancyname() if fancyname else self.name
        # Get Dagman submit file directory
        path = None
        dir_env_var = os.getenv('PYCONDOR_SUBMIT_DIR')
        if self.submit is not None:
            path = self.submit
        elif dir_env_var:
            path = dir_env_var
        # Create Dagman submit file path
        submit_file = os.path.join(path if path else '',
                                   '{}.submit'.format(name))
        # submit_file = '{}/{}.submit'.format(self.submit, name)
        self.submit_file = submit_file
        self.submit_name = name
        utils.checkdir(self.submit_file, makedirs)

        # Write dag submit file
        self.logger.info('Building DAG submission file {}...'.format(
            self.submit_file))
        lines = []
        parent_child_lines = []
        for node_index, node in enumerate(self, start=1):
            self.logger.info('Working on {} [{} of {}]'.format(node.name,
                             node_index, len(self.nodes)))
            # Build the BaseNode submit file
            if isinstance(node, Job):
                # node must be built before _get_job_arg_lines is called
                node._build_from_dag(makedirs, fancyname)
                # Add Job variables to Dagman submit file
                job_arg_lines = _get_job_arg_lines(node, fancyname)
                lines.extend(job_arg_lines)
            elif isinstance(node, Dagman):
                node.build(makedirs, fancyname)
                subdag_string = _get_subdag_string(node)
                lines.append(subdag_string)
            else:
                raise TypeError('Nodes must be either a Job or Dagman object')
            # Add parent/child information, if necessary
            if node.hasparents():
                parent_child_string = _get_parent_child_string(node)
                parent_child_lines.append(parent_child_string)

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            lines.extend(self.extra_lines)

        # Write lines to dag submit file
        with open(submit_file, 'w') as dag:
            dag.writelines('\n'.join(lines + ['\n#Inter-job dependencies'] +
                                     parent_child_lines))

        self._built = True
        self.logger.info('Dagman submission file for {} successfully '
                         'built!'.format(self.name))

        return self

    def submit_dag(self, maxjobs=3000, **kwargs):
        """Submits Dagman to condor

        Parameters
        ----------
        maxjobs : int, optional
            Maximum number of jobs to have running at a single time
            (default is 3000).

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
        # Construct and execute condor_submit_dag command
        command = 'condor_submit_dag -maxjobs {} {}'.format(
            maxjobs, self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out)

        return

    def build_submit(self, makedirs=True, fancyname=True, maxjobs=3000,
                     **kwargs):
        """Calls build and submit sequentially

        Parameters
        ----------
        makedirs : bool, optional
            If Job directories (e.g. error, output, log, submit) don't exist,
            create them (default is ``True``).

        fancyname : bool, optional
            Appends the date and unique id number to error, log, output, and
            submit files. For example, instead of ``dagname.submit`` the submit
            file becomes ``dagname_YYYYMMD_id``. This is useful when running
            several Dags/Jobs of the same name (default is ``True``).

        maxjobs : int, optional
            Maximum number of jobs to have running at a single time
            (default is 3000).

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
        self.submit_dag(maxjobs, **kwargs)

        return
