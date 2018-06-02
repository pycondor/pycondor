.. _subdags:

:github_url: https://github.com/jrbourbeau/pycondor

*****************
Creating a subdag
*****************

Assuming we have a directory where were would like our submit, log, etc. files
to be written to

.. code-block:: python

    submit = ...


we can create a Dagman  to submit to HTCondor.

.. code-block:: python

    from pycondor import Dagman

    dagman = Dagman(name='example_dagman',
                    submit=submit)

In a similar fashion to the way we can add a Job to a Dagman, we can also add
another Dagman to a Dagman (often referred to as a sub-Dagman or subdag). To
add a  subdag to a Dagman, we can make use of the ``dag`` parameter of the
Dagman object (exactly like when adding a Job to a Dagman). I.e.


.. code-block:: python

    sub_dagman = Dagman(name='example_subdag',
                        submit=submit,
                        dag=dagman)


In the same way that Dagman objects have an ``add_job`` method as an
alternative way to add Jobs to a Dagman, they also have an ``add_subdag``
method as a way to add subdags to a Dagman. I.e.
``dagman.add_subdag(sub_dagman)`` is another way to add a subdag to a
Dagman. See the :ref:`Dagman API documentation <dagman-api>` for more
information.
