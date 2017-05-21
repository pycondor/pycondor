
import os
import subprocess

from . import base
from .job import Job

def _get_parent_child_string(job):

    if not isinstance(job, Job):
        raise ValueError('Expecting a Job object, got {}'.format(type(job)))

    parent_string = 'Parent'
    for parentjob in job.parents:
        for parent_arg_idx in range(len(parentjob)):
            parent_string += ' {}_arg_{}'.format(parentjob.name, parent_arg_idx)

    child_string = 'Child'
    for job_arg_idx in range(len(job)):
        child_string += ' {}_arg_{}'.format(job.name, job_arg_idx)

    parent_child_string = parent_string + ' ' + child_string

    return parent_child_string


def _get_job_arg_lines(job, fancyname):

    if not isinstance(job, Job):
        raise ValueError('Expecting a Job object, got {}'.format(type(job)))

    job_arg_lines = []
    for idx, job_arg in enumerate(job):
        arg, name, retry = job_arg
        job_arg_lines.append('JOB {}_arg_{} '.format(job.name, idx) + job.submit_file)
        job_arg_lines.append('VARS {}_arg_{} '.format(job.name, idx) +
                  'ARGS={}'.format(base.string_rep(arg, quotes=True)))
        # Define job_name variable if there are arg_names present for this Job
        if not job._has_arg_names:
            pass
        elif name is not None:
            job_name = job._get_fancyname() if fancyname else job.name
            job_name += '_{}'.format(name)
            job_name = base.string_rep(job_name, quotes=True)
            job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(job.name, idx, job_name))
        else:
            job_name = job._get_fancyname() if fancyname else job.name
            job_name = base.string_rep(job_name, quotes=True)
            job_arg_lines.append('VARS {}_arg_{} job_name={}'.format(job.name, idx, job_name))
        # Add retry option for Job
        if retry is not None:
            job_arg_lines.append('Retry {}_arg_{} {}'.format(job.name, idx, retry))

    return job_arg_lines


class Dagman(base.SubmitFile):

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

    def __len__(self):
        return len(self.jobs)

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

        # Create DAG submit file path
        name = self._get_fancyname() if fancyname else self.name
        submit_file = '{}/{}.submit'.format(self.submit, name)
        self.submit_file = submit_file
        base.checkdir(self.submit_file, makedirs)

        # Write dag submit file
        self.logger.info('Building DAG submission file {}...'.format(self.submit_file))
        lines = []
        for job_index, job in enumerate(self, start=1):
            self.logger.info('Working on Job {} [{} of {}]'.format(
                job.name, job_index, len(self.jobs)))
            # Build the Job submit file
            job._build_from_dag(makedirs, fancyname)
            # Add Job variables to Dagman submit file
            job_arg_lines = _get_job_arg_lines(job, fancyname)
            lines.extend(job_arg_lines)
            # Add parent/child information, if necessary
            if job.hasparents():
                parent_child_string = _get_parent_child_string(job)
                lines.append(parent_child_string)

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            lines.extend(self.extra_lines)

        # Write lines to dag submit file
        with open(submit_file, 'w') as dag:
            dag.writelines('\n'.join(lines))

        self._built = True
        self.logger.info('DAGMan submission file for {} successfully '
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
