
import os
import subprocess

from . import utils
from .basenode import BaseNode
from .job import Job


def _get_subdag_string(dagman):

    if not isinstance(dagman, Dagman):
        raise ValueError('Expecting a Dagman object, got {}'.format(type(dagman)))

    subdag_string = 'SUBDAG EXTERNAL {} {}'.format(dagman.name, dagman.submit_file)

    return subdag_string


def _get_job_arg_lines(job, fancyname):

    if not isinstance(job, Job):
        raise ValueError('Expecting a Job object, got {}'.format(type(job)))

    job_arg_lines = []
    for idx, job_arg in enumerate(job):
        arg, name, retry = job_arg
        job_arg_lines.append('JOB {}_arg_{} '.format(job.name, idx) + job.submit_file)
        job_arg_lines.append('VARS {}_arg_{} '.format(job.name, idx) +
                  'ARGS={}'.format(utils.string_rep(arg, quotes=True)))
        # Define job_name variable if there are arg_names present for this Job
        if not job._has_arg_names:
            pass
        elif name is not None:
            job_name = job._get_fancyname() if fancyname else job.name
            job_name += '_{}'.format(name)
            job_name = utils.string_rep(job_name, quotes=True)
            job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(job.name, idx, job_name))
        else:
            job_name = job._get_fancyname() if fancyname else job.name
            job_name = utils.string_rep(job_name, quotes=True)
            job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(job.name, idx, job_name))
        # Add retry option for Job
        if retry is not None:
            job_arg_lines.append('Retry {}_arg_{} {}'.format(job.name, idx, retry))

    return job_arg_lines


def _get_parent_child_string(node):

    if not isinstance(node, BaseNode):
        raise ValueError('Expecting a Job or Dagman object, got {}'.format(type(job)))

    parent_string = 'Parent'
    for parent_node in node.parents:
        if isinstance(parent_node, Job):
            for parent_arg_idx in range(len(parent_node)):
                parent_string += ' {}_arg_{}'.format(parent_node.name, parent_arg_idx)
        else:
            parent_string += ' {}'.format(parent_node.name)

    child_string = 'Child'
    if isinstance(node, Job):
        for node_arg_idx in range(len(node)):
            child_string += ' {}_arg_{}'.format(node.name, node_arg_idx)
    else:
        child_string += ' {}'.format(node.name)

    parent_child_string = parent_string + ' ' + child_string

    return parent_child_string



class Dagman(BaseNode):

    def __init__(self, name, submit=None, extra_lines=None, verbose=0):

        super(Dagman, self).__init__(name, submit, extra_lines, verbose)

        self.nodes = []
        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'nodes', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Dagman(name={}, n_nodes={}{})'.format(self.name, len(self.nodes), nondefaults)

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
        self._add_node(job)

        return self

    def add_subdag(self, dag):
        self._add_node(dag)

        return self

    def build(self, makedirs=True, fancyname=True):

        if self._built:
            self.logger.warning(
                    '{} submit file has already been built. '
                    'Skipping the build process...'.format(self.name))
            return self

        # Create DAG submit file path
        name = self._get_fancyname() if fancyname else self.name
        submit_file = '{}/{}.submit'.format(self.submit, name)
        self.submit_file = submit_file
        utils.checkdir(self.submit_file, makedirs)

        # Write dag submit file
        self.logger.info('Building DAG submission file {}...'.format(self.submit_file))
        lines = []
        parent_child_lines = []
        for node_index, node in enumerate(self, start=1):
            self.logger.info('Working on {} [{} of {}]'.format(node.name, node_index, len(self.nodes)))
            # Build the BaseNode submit file
            if isinstance(node, Job):
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
            dag_lines = lines + ['\n#Inter-job dependencies'] + parent_child_lines
            dag.writelines('\n'.join(dag_lines))

        self._built = True
        self.logger.info('Dagman submission file for {} successfully '
                         'built!'.format(self.name))

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
