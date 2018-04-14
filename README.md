# PyCondor (Python HTCondor)

[![Build Status](https://travis-ci.org/jrbourbeau/pycondor.svg?branch=master)](https://travis-ci.org/jrbourbeau/pycondor)
[![codecov](https://codecov.io/gh/jrbourbeau/pycondor/branch/master/graph/badge.svg)](https://codecov.io/gh/jrbourbeau/pycondor)
![pypi version](https://img.shields.io/pypi/v/pycondor.svg 'pypi version')
![license](https://img.shields.io/pypi/l/pycondor.svg 'license')
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycondor.svg)

[HTCondor](https://research.cs.wisc.edu/htcondor/) is a an open-source workload management system for high throughput computing developed at the University of Wisconsin–Madison. PyCondor is a tool to help **build and submit HTCondor submission files in a straight-forward manner with minimal hassle**.


## Useful Links

* Documentation: https://jrbourbeau.github.io/pycondor
* PyPI: https://pypi.org/project/PyCondor/
* Release notes: https://jrbourbeau.github.io/pycondor/changelog.html
* Contributing: https://jrbourbeau.github.io/pycondor/contributing.html


## Installation

### Release version

PyCondor can be easily installed via `pip`

```
pip install pycondor
```

### Development version

The latest development version of PyCondor can be installed directly from GitHub

```
pip install git+https://github.com/jrbourbeau/pycondor.git
```

or you can always fork the [GitHub repository](https://github.com/jrbourbeau/pycondor) and install PyCondor on your local machine via

```
git clone https://github.com/<your-username>/pycondor.git
pip install pycondor
```


## Examples

For example uses of PyCondor, please see the [examples page](https://jrbourbeau.github.io/pycondor/examples.html) in the documentation or the `examples/` directory in the project repository.


## Contributing

To contribute to PyCondor, please see the [contributing page](https://jrbourbeau.github.io/pycondor/contributing.html) in the documentation.


## License

[MIT License](LICENSE)

Copyright (c) 2018 James Bourbeau
