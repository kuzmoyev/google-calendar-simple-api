from setuptools import setup, find_packages, Command
from sphinx.setup_command import BuildDoc
from shutil import rmtree
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.1.0'


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
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


class Doctest(Command):
    description = 'Run doctests with Sphinx'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sphinx.application import Sphinx
        sph = Sphinx('./docs/source',  # source directory
                     './docs/source',  # directory containing conf.py
                     './docs/build',  # output directory
                     './docs/build/doctrees',  # doctree directory
                     'doctest')  # finally, specify the doctest builder
        sph.build()


with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='gcsa',
    version=VERSION,
    keywords='google calendar simple api recurrence',
    description='Simple API for Google Calendar management',
    long_description=long_description,
    author='Yevhen Kuzmovych',
    author_email='kuzmovych.yevhen@gmail.com',
    license='MIT',
    url='https://github.com/kuzmoyev/google-calendar-simple-api',
    zip_safe=False,
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "tzlocal>=2,<3",
        "google-api-python-client>=1.8",
        "google-auth-httplib2>=0.0.4",
        "google-auth-oauthlib>=0.4,<0.5",
        "python-dateutil>=2.7",
        "beautiful_date>=2.0.0",
    ],
    tests_require=[
        "pytest>=5.4",
        "pytest-cov>=2.10",
        "flake8>3.8.3",
        "pep8-naming>=0.11.1",
        "pyfakefs>=4.3.1,<5.0",
    ],
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
    ],
    cmdclass={
        'upload': UploadCommand,
        'build_sphinx': BuildDoc,
        'doctest': Doctest
    }
)
