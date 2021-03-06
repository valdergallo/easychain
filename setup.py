# encoding: utf-8
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import easychain


def readme():
    try:
        os.system('pandoc --from=markdown --to=rst README.md -o README.rst')
        with open('README.rst') as f:
            return f.read()
    except Exception:
        return '''This is the result of a bit of research and some tinkering to understand the fundamental concepts of a blockchain. Readers are directed to Ilya Gritorik's fantastic Minimum Viable Blockchain article for more general information about what blockchains are and how they work conceptually.'''


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['easychain', 'tests', '-vrsx']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='easychain',
    url='https://github.com/valder/easychain',
    download_url='https://github.com/valder/easychain/tarball/{0!s}/'.format(
        easychain.__version__),
    author="valdergallo, davecan",
    author_email='valdergallo@gmail.com',
    keywords='blockchain, bitcoin',
    description='Simple library to easily export blockchain',
    license='MIT',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    version=easychain.__version__,
    cmdclass={'test': PyTest},
    zip_safe=False,
    platforms='any',
    package_dir={'': '.'},
    packages=find_packages(
        '.', exclude=['tests', '*.tests', 'docs', 'example.py']),
)
