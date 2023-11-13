#!/usr/bin/env python3

from setuptools import setup, find_packages, Command
from shutil import rmtree
import os
import sys

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    class BuildDoc(Command):
        user_options = []

        def run(self):
            raise

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '2.2.0'


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        error = os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
        if error:
            sys.exit()

        self.status('Uploading the package to PyPi via Twine...')
        error = os.system('twine upload dist/*')
        if error:
            sys.exit()

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


with open('README.rst') as f:
    long_description = ''.join(f.readlines())

DOCS_REQUIRES = [
    'sphinx',
    'sphinx-rtd-theme',
]

TEST_REQUIRES = [
    'setuptools',
    'pytest',
    'pytest-pep8',
    'pytest-cov',
    'pyfakefs',
    'flake8',
    'pep8-naming',
    'twine',
    'tox'
]

setup(
    name='gcsa',
    version=VERSION,
    keywords='python conference calendar hangouts python-library event conferences google-calendar pip recurrence '
             'google-calendar-api attendee gcsa',
    description='Simple API for Google Calendar management',
    long_description=long_description,
    author='Yevhen Kuzmovych',
    author_email='kuzmovych.yevhen@gmail.com',
    license='MIT',
    url='https://github.com/kuzmoyev/google-calendar-simple-api',
    zip_safe=False,
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "tzlocal>=4,<5",
        "google-api-python-client>=1.8",
        "google-auth-httplib2>=0.0.4",
        "google-auth-oauthlib>=0.5,<1.0",
        "python-dateutil>=2.7",
        "beautiful_date>=2.0.0",
    ],
    extras_require={
        'dev': [
            *TEST_REQUIRES,
            *DOCS_REQUIRES
        ],
        'tests': TEST_REQUIRES,
        'docs': DOCS_REQUIRES
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    cmdclass={
        'upload': UploadCommand,
        'docs': BuildDoc,
    },
    command_options={
        'docs': {
            'version': ('setup.py', VERSION),
            'build_dir': ('setup.py', 'docs/build')
        }
    },
)
