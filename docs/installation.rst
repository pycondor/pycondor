.. _installation:

:github_url: https://github.com/pycondor/pycondor

************
Installation
************

----
PyPI
----

The latest release of PyCondor can be installed with ``pip``:

.. code-block:: bash

    pip install pycondor

This installs PyCondor, along with all the necessary dependencies.


-----
Conda
-----

PyCondor is available on `conda-forge <https://anaconda.org/conda-forge/pycondor>`_ and can be installed with ``conda``:

.. code-block:: bash

    conda install -c conda-forge pycondor

This installs PyCondor, along with all the necessary dependencies.


-------------------
Development Version
-------------------

The latest development version of PyCondor can be install directly from GitHub

.. code-block:: bash

    pip install git+https://github.com/pycondor/pycondor.git


or you can fork the `PyCondor GitHub repository <https://github.com/pycondor/pycondor>`_ and install PyCondor on your local machine via

.. code-block:: bash

    git clone https://github.com/<your-username>/pycondor.git
    pip install pycondor


------------
Dependencies
------------

PyCondor has the following dependencies:

- `Python <https://www.python.org/>`_ >= 2.7 or >= 3.4
- `click <https://github.com/pallets/click>`_

You can use ``pip`` or ``conda`` to install these automatically.
