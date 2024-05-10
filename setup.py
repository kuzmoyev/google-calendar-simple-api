#!/usr/bin/env python3
import subprocess

from setuptools import setup, find_packages, Command
from shutil import rmtree
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '2.3.0'


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


class BuildDoc(Command):
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self):
        output_path = 'docs/html'
        changed_files = []
        cmd = [
            'sphinx-build',
            'docs/source', output_path,
            '--builder', 'html',
            '--define', f'version={VERSION}',
            '--verbose'
        ]
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')
                if line.startswith('reading sources... ['):
                    file_name = line.rsplit(maxsplit=1)[1]
                    if file_name:
                        changed_files.append(file_name + '.html')

        index_path = os.path.join(os.getcwd(), output_path, 'index.html')
        print('\nIndex:')
        print(f'file://{index_path}')

        if changed_files:
            print('Update pages:')
            for cf in changed_files:
                f_path = os.path.join(os.getcwd(), output_path, cf)
                print(cf, f'file://{f_path}')


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
        "google-auth-oauthlib>=0.5,<2.0",
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
        'Programming Language :: Python :: 3.12',
    ],
    cmdclass={
        'upload': UploadCommand,
        'docs': BuildDoc,
    }
)
