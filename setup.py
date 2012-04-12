#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2011 Daniel Holth
# 
# Derived from original pyzmq © 2010 Brian Granger
#
# This file is part of pyzmq-ctypes
#
# pyzmq-ctypes is free software; you can redistribute it and/or modify it
# under the terms of the Lesser GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pyzmq-ctypes is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU General Public
# License for more details.
#
# You should have received a copy of the Lesser GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import os, sys
import copy
import re
import shutil
from traceback import print_exc

from distutils.core import setup, Command
from distutils.ccompiler import get_default_compiler
from distutils.extension import Extension
from distutils.errors import CompileError, LinkError
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.sdist import sdist
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin

from subprocess import Popen, PIPE
import logging

try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

try:
    import nose
except ImportError:
    nose = None

# local script imports:
from buildutils import (discover_settings, v_str, localpath, savepickle, loadpickle, detect_zmq,
                        warn, fatal, copy_and_patch_libzmq)

class TestCommand(Command):
    """Custom distutils command to run the test suite."""

    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run_nose(self):
        """Run the test suite with nose."""
        return nose.core.TestProgram(argv=["", '-vv', pjoin(self._dir, 'zmq', 'tests')])
    
    def run_unittest(self):
        """Finds all the tests modules in zmq/tests/ and runs them."""
        testfiles = [ ]
        for t in glob(pjoin(self._dir, 'zmq', 'tests', '*.py')):
            name = splitext(basename(t))[0]
            if name.startswith('test_'):
                testfiles.append('.'.join(
                    ['zmq.tests', name])
                )
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 2)
        t.run(tests)

    def run(self):
        """Run the test suite, with nose, or unittest if nose is unavailable"""
        # crude check for inplace build:
        try:
            import zmq
        except ImportError:
            print_exc()
            fatal('\n       '.join(["Could not import zmq!",
            "You must build pyzmq with 'python setup.py build_ext --inplace' for 'python setup.py test' to work.",
            "If you did build pyzmq in-place, then this is a real error."]))
            sys.exit(1)

        if nose is None:
            print ("nose unavailable, falling back on unittest. Skipped tests will appear as ERRORs.")
            return self.run_unittest()
        else:
            return self.run_nose()

cmdclass = {'test': TestCommand}


long_desc = \
"""
pyzmq-ctypes is a ctypes binding for the ZeroMQ library
(http://www.zeromq.org) that will run on pypy.
"""

setup(
    name = "pyzmq-ctypes",
    version = "2.1.7",
    packages = ['zmq', 'zmq.core', 'zmq.utils'],
    author = "Daniel Holth",
    author_email = "dholth@fastmail.fm",
    url = 'http://github.com/svpcom/pyzmq-ctypes',
    download_url = 'http://python.org/pypi/pyzmq-ctypes',
    description = "Python bindings for 0MQ (ctypes version).",
    install_requires = ['ctypes_configure'],
    long_description = long_desc,
    license = "LGPL",
    cmdclass = cmdclass,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX',
        'Topic :: System :: Networking'
    ]
)

