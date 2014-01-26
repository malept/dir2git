Directory to Git Repository
===========================

Wrote some code a long time ago but forgot to commit it? Retcon it with
``dir2git``!

How Does It Work?
-----------------

Give the script a directory, and it will collect committable files and their
last modified timestamps. It will then commit the files, grouped by last
modified date.

Install
-------

Requirements:

* Python 2.6, 2.7, 3.3, or PyPy
* Dulwich_
* python-dateutil_

.. _Dulwich: https://www.samba.org/~jelmer/dulwich/
.. _python-dateutil: http://labix.org/python-dateutil

Usage
-----

Run ``dir2git.py --help`` for details.

License
-------

This project is licensed under the GNU Public License 3.0 or later. See ``LICENSE`` for details.
