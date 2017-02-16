=======
Revived
=======

.. image:: https://travis-ci.org/RookieGameDevs/revived.svg?branch=master
   :target: https://travis-ci.org/RookieGameDevs/revived

.. image:: https://codecov.io/gh/RookieGameDevs/revived/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/RookieGameDevs/revived

.. image:: https://readthedocs.org/projects/revived/badge/?version=latest
   :target: http://revived.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

---------------------------------------------------------------------
A predictable state container for python *heavily* inspired by Redux_
---------------------------------------------------------------------

While not being a *strict 1:1 port* of `Redux API`_, **Revived** is supposed to
do pretty much the same job in the most pythonic way possible.

**NOTE**: I needed this piece of code to work with the **latest python available
at the moment** (3.6). While I am not really caring about other versions, the
Travis build is running the test suites on **all the 3.5+ versions**, including
the dev ones.

Contents
--------
* Documentation_
* Installation_
* Examples_
* Contribute_

Documentation
-------------

Currently the documentation is not buliding into ReadTheDocs (see
`issue #11 <https://github.com/RookieGameDevs/revived/issues/11>`_). You can
build the documentation locally. Check out Contribute_ section.

Installation
------------

**Revived** package is available on pypi: to install it use the following
command::

   pip install revived

Examples
--------

Usage examples are **coming soon**.

Contribute
----------

#. Clone the repository.
#. Create the virtualenv.

   * using virtualenv_::

      virtualenv ENV
      bin/activate

   * using virtualfish_::

      vf new ENV
      # optional: automatically load the virtualenv when entering the dir
      vf connect

#. Install the dependencies::

    pip install -r requirements.txt

#. Build the documentation::

    cd docs
    make html  # or whatever format you prefer

#. Work on the revived module.
#. Write tests.
#. Run tests::

    # to have coverage in command line
    pytest --cov revived --pep8 revived tests

    # to have html coverage file in the htmlcov directory
    pytest --cov revived --cov-report html --pep8 revived tests

#. Check type hints::

    mypy revived tests

#. Create a pull request.
#. Profit :)

.. _Redux: http://redux.js.org/
.. _`Redux API`: Redux_
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _virtualfish: http://virtualfish.readthedocs.io/en/latest/
