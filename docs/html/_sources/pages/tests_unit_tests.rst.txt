Unit Tests
=======================================================

Testing is also done using unit tests. With this method it is not possible to test all the functions of the module without significant overhead, so for some functionality it is still necessary to test manually using functional tests.

For unit tests, the module installed as an add-on has a set of operators that test each function separately and a main operator that runs all available unit tests.

The following is an example of how testing can be run.

.. image:: ../images/test_unit_tests.gif
    :align: center

Obviously, if you want to make any changes to the main repository, these changes should not destroy existing unit tests. For the new functionality - it is very desirable to write new unit tests.