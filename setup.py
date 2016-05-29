#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import unittest


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tvdb_client.tests import client

        login_tests = client.LoginTestCase()
        search_tests = client.SearchTestCase()

        tests = (login_tests, search_tests)

        for t in tests:
            test_loader = unittest.TestLoader()
            test_runner = unittest.TextTestRunner()
            suite = test_loader.loadTestsFromTestCase(t)
            errno = test_runner.run(suite)
            if errno != 0:
                sys.exit(errno)

        sys.exit(0)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'tvdb_client',
    'tvdb_client.clients',
    'tvdb_client.exceptions',
    'tvdb_client.tests',
    'tvdb_client.utils'
]

requires = ['requests', 'lxml']
test_requirements = ['nose']

with open('tvdb_client/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
# with open('HISTORY.rst', 'r', 'utf-8') as f:
#     history = f.read()

setup(
    name='tvdb_client',
    version=version,
    description='TheTVDB Client API Library',
    long_description=readme + '\n\n',
    author='Thiago Santana',
    author_email='thilux.systems@gmail.com',
    url='https://github.com/thilux/tvdb_client',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},
    package_dir={'tvdb_client': 'tvdb_client'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    test_suite='nose.collector',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    # cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
