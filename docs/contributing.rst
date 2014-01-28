Contributing
============

Process
-------

As an open source project, ``cryptography`` welcomes contributions of all
forms. These can include:

* Bug reports and feature requests
* Pull requests for both code and documentation
* Patch reviews

You can file bugs and submit pull requests on `GitHub`_. To discuss larger
changes you can start a conversation on `our mailing list`_.

Because cryptography is so complex, and the implications of getting it wrong so
devastating, ``cryptography`` has a strict code review policy:

* Patches must *never* be pushed directly to ``master``, all changes (even the
  most trivial typo fixes!) must be submitted as a pull request.
* A committer may *never* merge their own pull request, a second party must
  merge their changes. If multiple people work on a pull request, it must be
  merged by someone who did not work on it.
* A patch which breaks tests, or introduces regressions by changing or removing
  existing tests should not be merged. Tests must always be passing on
  ``master``.
* If somehow the tests get into a failing state on ``master`` (such as by a
  backwards incompatible release of a dependency) no pull requests may be
  merged until this is rectified.
* All merged patches must have 100% test coverage.
* New features and significant bug fixes should be documented in the
  :doc:`/changelog`.

The purpose of these policies is to minimize the chances we merge a change
which jeopardizes our users' security.

If you believe you've identified a security issue in ``cryptography``, please
follow the directions on the :doc:`security page </security>`.

Code
----

When in doubt, refer to `PEP 8`_ for Python code.

Every code file must start with the boilerplate notice of the Apache License.
Additionally, every Python code file must contain

.. code-block:: python

    from __future__ import absolute_import, division, print_function

API Considerations
~~~~~~~~~~~~~~~~~~

Most projects' APIs are designed with a philosophy of "make easy things easy,
and make hard things possible". One of the perils of writing cryptographic code
is that secure code looks just like insecure code, and its results are almost
always indistinguishable. As a result ``cryptography`` has, as a design
philosophy: "make it hard to do insecure things". Here are a few strategies for
API design which should be both followed, and should inspire other API choices:

If a user will need to compare a user provided value with a computed value (for
example, checking a signature on something), there should be an API provided
which performs the check for the user in a secure way (for example, using a
constant time comparison), rather than requiring the user to perform the
comparison themselves.

If it is incorrect to ignore the result of a method, it should raise an
exception, and not return a boolean ``True``/``False`` flag. For example, a
method to verify a signature should raise ``InvalidSignature``, and not return
whether the signature was valid.

.. code-block:: python

    # This is bad.
    def verify(sig):
        # ...
        return is_valid

    # Good!
    def verify(sig):
        # ...
        if not is_valid:
            raise InvalidSignature

Every recipe should include a version or algorithmic marker of some sort in its
output in order to allow transparent upgrading of the algorithms in use, as
the algorithms or parameters needed to achieve a given security margin evolve.

APIs at the :doc:`/hazmat/primitives/index` layer should always take an
explicit backend, APIs at the recipes layer should automatically use the
:func:`~cryptography.hazmat.backends.default_backend`, but optionally allow
specifying a different backend.

C bindings
~~~~~~~~~~

When binding C code with ``cffi`` we have our own style guide, it's pretty
simple.

Don't name parameters:

.. code-block:: c

    // Good
    long f(long);
    // Bad
    long f(long x);

...unless they're inside a struct:

.. code-block:: c

    struct my_struct {
        char *name;
        int number;
        ...;
    };

Include ``void`` if the function takes no arguments:

.. code-block:: c

    // Good
    long f(void);
    // Bad
    long f();

Wrap lines at 80 characters like so:

.. code-block:: c

    // Pretend this went to 80 characters
    long f(long, long,
           int *)

Include a space after commas between parameters:

.. code-block:: c

    // Good
    long f(int, char *)
    // Bad
    long f(int,char *)

Values set by ``#define`` should be assigned the appropriate type. If you see
this:

.. code-block:: c

    #define SOME_INTEGER_LITERAL 0x0;
    #define SOME_UNSIGNED_INTEGER_LITERAL 0x0001U;
    #define SOME_STRING_LITERAL "hello";

...it should be added to the bindings like so:

.. code-block:: c

    static const int SOME_INTEGER_LITERAL;
    static const unsigned int SOME_UNSIGNED_INTEGER_LITERAL;
    static const char *const SOME_STRING_LITERAL;

Documentation
-------------

All features should be documented with prose.

Docstrings should be written like this:

.. code-block:: python

    def some_function(some_arg):
        """
        Does some things.

        :param some_arg: Some argument.
        """

So, specifically:

* Always use three double quotes.
* Put the three double quotes on their own line.
* No blank line at the end.
* Use Sphinx parameter/attribute documentation `syntax`_.

Because of the inherent challenges in implementing correct cryptographic
systems, we want to make our documentation point people in the right directions
as much as possible. To that end:

* When documenting a generic interface, use a strong algorithm in examples.
  (e.g. when showing a hashing example, don't use
  :class:`~cryptography.hazmat.primitives.hashes.MD5`)
* When giving prescriptive advice, always provide references and supporting
  material.
* When there is real disagreement between cryptographic experts, represent both
  sides of the argument and describe the trade-offs clearly.

When documenting a new module in the ``hazmat`` package, its documentation
should begin with the "Hazardous Materials" warning:

.. code-block:: rest

    .. hazmat::

When referring to a hypothetical individual (such as "a person receiving an
encrypted message") use gender neutral pronouns (they/them/their).

Development Environment
-----------------------

Working on ``cryptography`` requires the installation of a small number of
development dependencies. These are listed in ``dev-requirements.txt`` and they
can be installed in a `virtualenv`_ using `pip`_. Once you've installed the
dependencies, install ``cryptography`` in ``editable`` mode. For example:

.. code-block:: console

   $ # Create a virtualenv and activate it
   $ pip install --requirement dev-requirements.txt
   $ pip install --editable .

You are now ready to run the tests and build the documentation.

Running Tests
~~~~~~~~~~~~~

``cryptography`` unit tests are found in the ``tests/`` directory and are
designed to be run using `pytest`_. `pytest`_ will discover the tests
automatically, so all you have to do is:

.. code-block:: console

   $ py.test
   ...
   62746 passed in 220.43 seconds

This runs the tests with the default Python interpreter.

You can also verify that the tests pass on other supported Python interpreters.
For this we use `tox`_, which will automatically create a `virtualenv`_ for
each supported Python version and run the tests. For example:

.. code-block:: console

   $ tox
   ...
   ERROR:   py26: InterpreterNotFound: python2.6
    py27: commands succeeded
   ERROR:   pypy: InterpreterNotFound: pypy
   ERROR:   py32: InterpreterNotFound: python3.2
    py33: commands succeeded
    docs: commands succeeded
    pep8: commands succeeded

You may not have all the required Python versions installed, in which case you
will see one or more ``InterpreterNotFound`` errors.


Explicit Backend Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~

While testing you may want to run tests against a subset of the backends that
cryptography supports. Explicit backend selection can be done via the
``--backend`` flag. This flag should be passed to ``py.test`` with a comma
delimited list of backend names. To use it with ``tox`` you must pass it as
``tox -- --backend=openssl``.

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

``cryptography`` documentation is stored in the ``docs/`` directory. It is
written in `reStructured Text`_ and rendered using `Sphinx`_.

Use `tox`_ to build the documentation. For example:

.. code-block:: console

   $ tox -e docs
   ...
   docs: commands succeeded
   congratulations :)

The HTML documentation index can now be found at
``docs/_build/html/index.html``.


.. _`GitHub`: https://github.com/pyca/cryptography
.. _`our mailing list`: https://mail.python.org/mailman/listinfo/cryptography-dev
.. _`PEP 8`: http://www.peps.io/8/
.. _`syntax`: http://sphinx-doc.org/domains.html#info-field-lists
.. _`pytest`: https://pypi.python.org/pypi/pytest
.. _`tox`: https://pypi.python.org/pypi/tox
.. _`virtualenv`: https://pypi.python.org/pypi/virtualenv
.. _`pip`: https://pypi.python.org/pypi/pip
.. _`sphinx`: https://pypi.python.org/pypi/Sphinx
.. _`reStructured Text`: http://sphinx-doc.org/rest.html
