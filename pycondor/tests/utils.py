
import os


def clear_pycondor_environment_variables():
    # Unset any pycondor directory environment variables
    for i in ['submit', 'output', 'error', 'log']:
        os.environ['PYCONDOR_{}_DIR'.format(i.upper())] = ''
