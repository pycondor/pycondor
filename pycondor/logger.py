#!/usr/bin/env python

import logging

# Specify logging settings
logging.basicConfig(
    format='%(levelname)s: dagmanager - %(name)s : %(message)s')
logging_level_dict = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def setup_logger(cls, verbose):
    """Configures and returns logger instance.

    This function takes a class instance (which must have a `name` attribute)
    and a verbosity level as parameters and returns a connfigured logger
    instance with the appropriate level set.

    Parameters
    ----------
    cls : object
        dagmanager class instance with attribute `name` (e.g. CondorExecutable,
        CondorJob, DagManager)
    verbose: int
        Verbosity level. Values can be 0, 1, or 2, with 0 being the least
        verbose and 2 being the most verbose.

    Returns
    -------
    logger : logging.Logger
        Configured logger

    The dagmanager classes each have their own seperate loggers in order to
    allow for varying levels of verbosity. For example, you might want low
    verbosity for CondorExecutable classes, but high verbosity for DagManager
    classes. setup_logger() helps streamline this process.
    """
    # Set up logger
    if verbose not in logging_level_dict:
        raise KeyError('Verbose option {} for {} not valid. Valid options are {}.'.format(
            verbose, cls.name, logging_level_dict.keys()))
    logger = logging.getLogger(cls.name)
    logger.setLevel(logging_level_dict[verbose])

    return logger
