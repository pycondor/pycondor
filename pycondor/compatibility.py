# flake8: noqa
import sys


PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2

if PY3:
    string_types = (str,)
else:
    string_types = (basestring,)
