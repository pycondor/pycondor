.. _contributing:

:github_url: https://github.com/pycondor/pycondor

************
Contributing
************

PyCondor is an open source project and contributions are always welcome!

If you are new to working with forks, check out `GitHub's working with forks article <https://help.github.com/articles/working-with-forks/>`_.

============================
Step 1: Creating a new issue
============================

- If you don't already have a `GitHub <http://www.github.com>`_ account, create one
- Go to the `PyCondor GitHub page <https://github.com/pycondor/pycondor>`_ and create a new issue by clicking on the "Issues" tab and then the "New issue" button

.. image:: _static/open-new-issue.png

.. image:: _static/new-issue-button.png

==============================
Step 2: Forking the repository
==============================

(If you have an existing configured fork of PyCondor, you can skip to Step 4: Syncing an existing fork)

- From the PyCondor repository use the "Fork" button to fork the project into your GitHub account

.. image:: _static/fork-button.png

- This forked copy of PyCondor can now be cloned to your local machine using

.. code-block:: bash

    $ git clone https://github.com/<your_username>/pycondor.git

=======================================
Step 3: Configuring a remote for a fork
=======================================

From your cloned copy of PyCondor from the previous step, list the existing remotes with

.. code-block:: bash

    $ cd pycondor
    $ git remote -v


You'll most likely see something like

.. code-block:: bash

    origin  https://github.com/<your_username>/pycondor.git (fetch)
    origin  https://github.com/<your_username>/pycondor.git (push)


To add the original PyCondor project repository as a remote (named "upstream") to your copy of PyCondor via

.. code-block:: bash

    $ git remote add upstream https://github.com/pycondor/pycondor.git


Now when you execute ``git remote -v``, the newly added upstream remote should be present

.. code-block:: bash

    origin  https://github.com/<your_username>/pycondor.git (fetch)
    origin  https://github.com/<your_username>/pycondor.git (push)
    upstream        https://github.com/pycondor/pycondor.git (fetch)
    upstream        https://github.com/pycondor/pycondor.git (push)


================================
Step 4: Syncing an existing fork
================================

To ensure that your existing fork is up-to-date with the original PyCondor repository, fetch the upstream commits via

.. code-block:: bash

    $ git fetch upstream


The output should look something like

.. code-block:: bash

    remote: Counting objects: xx, done.
    remote: Compressing objects: 100% (xx/xx), done.
    remote: Total xx (delta xx), reused xx (delta x)
    Unpacking objects: 100% (xx/xx), done.
    From https://github.com/pycondor/pycondor
     * [new branch]      master     -> upstream/master


Now the commits to the master branch of pycondor/pycondor are stored in your local upstream/master branch. At this point, you'll want to make sure (if you're not already) that you're on the master branch of your local repository

.. code-block:: bash

    $ git checkout master
    Switched to branch 'master'


Now you can merge the upstream/master branch into your master branch with


.. code-block:: bash

    $ git merge upstream/master


Now the master branch of your local copy of PyCondor should be up-to-date with the original PyCondor master branch!

===================================
Step 5: Create a new feature branch
===================================

Next, create a new branch for the feature you would like to develop with

.. code-block:: bash

    $ git checkout -b <new_feature_branch_name>


The output should be

.. code-block:: bash

    Switched to branch '<new_feature_branch_name>'


======================================
Step 6: Install local copy of PyCondor
======================================

Next, you'll want to make sure that Python imports your local version of PyCondor. This can be done by ``pip`` installing your local PyCondor repository in `editable mode <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_

.. code-block:: bash

    $ pip install -e .

To install additional development dependencies for running tests and building the documentation, instead run

.. code-block:: bash

    $ pip install -e .[dev]

Note that if you previously had PyCondor installed in your environment to ``pip uninstall pycondor`` before executing the previous command.


=========================
Step 7: Develop new code!
=========================

Now add your feature, bug fix, typo fix, etc.


=======================================
Step 8: Running tests with the new code
=======================================

Once your contributions have been added, you’ll want to run the tests for this project to ensure that none of the new code breaks any existing tests. Tests can be run by going to the root directory of your pyunfold repository and executing

.. code-block:: bash

    pytest pycondor

To run with code coverage use ``pytest --cov pycondor``

=====================
Step 9: Documentation
=====================

If necessary for your contribution, add the appropriate documentation to the files in the ``docs/`` directory. The documentation can be build via

.. code-block:: bash

    cd docs
    make html

The built documentation will be placed in the ``_build/html`` directory.

=========================================
Step 10: Committing and uploading changes
=========================================

Now the changes you've made are ready to be committed and uploaded to GitHub. Let git know which files you would like to include in your commit via

.. code-block:: bash

    $ git add <modifies_files_here>


and then commit your changes with

.. code-block:: bash

    $ git commit -m '<meaningful messages about the changes made>'


Now you can push this commit from your local repository to your copy on GitHub

.. code-block:: bash

    $ git push origin <new_feature_branch_name>


==================================
Step 11: Submitting a pull request
==================================

Finally, you can go to your copy of PyCondor on GitHub and submit a pull request by clicking the "Compare & pull request" button!

.. image:: _static/pull-request-button.png
