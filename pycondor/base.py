
import os

def checkdir(path, makedirs):
    assert path is not None, 'path must me non-NoneType'
    outdir = os.path.dirname(path)
    if outdir == '':
        outdir = os.getcwd()
    if not os.path.isdir(outdir):
        if makedirs:
            print('The directory {} doesn\'t exist, '.format(outdir)
                  + 'creating it...')
            os.makedirs(outdir)
        else:
            raise OSError('The directory {} doesn\'t exist'.format(outdir))
    return


def list_queue():
    import subprocess
    proc = subprocess.Popen(["condor_q"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out
    

def string_rep(obj, quotes=False):
    '''Converts basic python objects to a string representation

    '''
    assert obj is not None, 'obj must not be None'

    quote = '"' if quotes else ''

    if isinstance(obj, (tuple, list)):
        obj_str = ', '.join([string_rep(item) for item in obj])
    else:
        obj_str = str(obj)

    return quote + obj_str + quote
