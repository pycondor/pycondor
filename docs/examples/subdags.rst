.. _subdags:

:github_url: https://github.com/pycondor/pycondor

*****************
Creating a subdag
*****************

Assuming we have a directory where were would like our submit files to be
written.

.. code-block:: python

    submit = ...


We can then create a Dagman to submit to HTCondor.

.. code-block:: python

    from pycondor import Dagman

    dagman = Dagman(name='example_dagman',
                    submit=submit)

Similarly to how we can add a Job to a Dagman, we can also add another Dagman
to a Dagman (often referred to as a "sub-Dagman" or "subdag"). To add a  subdag to
a Dagman, we can make use of the ``dag`` parameter of the Dagman object
(exactly like when adding a Job to a Dagman). I.e.


.. code-block:: python

    sub_dagman = Dagman(name='example_subdag',
                        submit=submit,
                        dag=dagman)



Alternatively, instead of using the ``dag`` parameter when instantiating a Job,
Dagman objects have an ``add_subdag`` method that can be used to add Jobs to a
Dagman. I.e. ``dagman.add_subdag(sub_dagman)`` is another way to add a subdag
to a Dagman. See the :ref:`Dagman API documentation <dagman-api>` for more
information.
