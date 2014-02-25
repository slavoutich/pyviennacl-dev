*****************
PyViennaCL Readme
*****************

PyViennaCL around the web
=========================

* `Home page <http://viennacl.sourceforge.net/pyviennacl.html>`_
* `Documentation <http://viennacl.sourceforge.net/pyviennacl/doc/index.html>`_
* `GitHub <https://github.com/viennacl/pyviennacl-dev>`_ (`Issue tracker <https://github.com/viennacl/pyviennacl-dev/issues>`_)

About PyViennaCL
================

*PyViennaCL* aims to make fast, powerful GPGPU and hetereogeneous
scientific computing really transparently easy, especially for users
already using NumPy for representing matrices.

PyViennaCL does this by harnessing the `ViennaCL
<http://viennacl.sourceforge.net/>`_ linear algebra and numerical computation
library for GPGPU and heterogeneous systems, thereby making available to Python
programmers ViennaCL’s fast *OpenCL* and *CUDA* algorithms. PyViennaCL does
this in a way that is idiomatic and compatible with the Python community’s most
popular scientific packages, *NumPy* and *SciPy*.

PyViennaCL exposes the following functionality:

* sparse (compressed, co-ordinate, ELL, and hybrid) and dense
  (row-major and column-major) matrices, vectors and scalars on your
  compute device using OpenCL;
* standard arithmetic operations and mathematical functions;
* fast matrix products for sparse and dense matrices, and inner and
  outer products for vectors;
* direct solvers for dense triangular systems;
* iterative solvers for sparse and dense systems, using the BiCGStab,
  CG, and GMRES algorithms;
* iterative algorithms for eigenvalue estimation problems.


Requirements
============

PyViennaCL requires the following build dependencies:

* *Python* (2.7+);
* *NumPy* (1.7+);
* *Sphinx* (1.0+) [if you want to build HTML documentation].

It is also highly recommended to have an available OpenCL
implementation, since PyViennaCL was designed for this case. If you do
not have OpenCL available, then PyViennaCL will still build and
function, but will not perform to full effect.

If you have a Boost installation on your system, then PyViennaCL can
also optionally use that, rather than the Boost subset shipped with
the PyViennaCL sources.


Installation
============

OpenCL
------

By default, you will need an OpenCL implementation. PyViennaCL will
still build and function without one, but will not perform to full
effect.

For information on how to get an OpenCL implementation, see this
`howto <http://wiki.tiker.net/OpenCLHowTo>`_.

If you do not wish to use OpenCL, then follow the *Installation from
source* instructions below, and use the '--no-use-opencl' configure
option.

Installation using pip
----------------------

The following command should usually be enough to install PyViennaCL::

  $> pip install pyviennacl

TODO: See `issue <https://github.com/viennacl/pyviennacl-dev/issues/2>`_.

Installation from source
------------------------

These instructions assume a UNIX-like platform (such as a Linux
distribution or Mac OS X), but will work on a well-configured Windows
system with little modification.

If you are building from git, then before doing anything else, you
should get the external submodules with::

  $> git submodule update --init

If you are in a hurry, then the following should just work::

  $> python setup.py build
  $> sudo python setup.py install

Otherwise, read the configuration options, configure, make and
install::

  $> ./configure.py --help
  $> ./configure.py --some-options
  $> make
  $> sudo make install

To build the HTML documentation using Sphinx, first install PyViennaCL
as above, and then run::

  $> cd doc
  $> make html

after which HTML documentation will be in doc/_build/html. Or you can
just access the documentation from within the Python interpreter after
installation::

  >>> import pyviennacl
  >>> help(pyviennacl)


Authors and Contact
===================

PyViennaCL was developed during the 2013 *Google Summer of Code* by 
`Toby St Clere Smithe <pyviennacl@tsmithe.net>`_.

ViennaCL was developed under the aegis of the *Institute for Microelectronics*
at the *Vienna University of Technology*.

For any technical questions related to ViennaCL, please use `our
mailing list <viennacl-support@lists.sourceforge.net>`_.

Licence
=======

(Py)ViennaCL is distributed under the MIT (X11) License. See the file
LICENSE in the source root directory.