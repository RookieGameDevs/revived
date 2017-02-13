=======
Revived
=======

---------------------------------------------------------------------
A predictable state container for python *heavily* inspired by Redux_
---------------------------------------------------------------------

While not being a *strict 1:1 port* of `Redux API`_, **Revived** is supposed to
do pretty much the same job in the most pythonic way possible.

**NOTE**: I needed this piece of code to work with the latest python available
(3.6) and *I did not really care about checking for the previous versions*.

Contents
--------
* Installation_
* Examples_
* Contribute_
* Documentation_

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

#. Work on the revived module.
#. Write tests.
#. Run tests::

    pytest tests

#. Check type hints::

    mypy revived tests

#. Create a pull request.
#. Profit :)

Documentation
-------------

More detailed documentation is **coming soon**.

.. _Redux: http://redux.js.org/
.. _`Redux API`: Redux_
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _virtualfish: http://virtualfish.readthedocs.io/en/latest/