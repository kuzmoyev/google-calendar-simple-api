from setuptools import setup, find_packages, Command
from sphinx.setup_command import BuildDoc
from shutil import rmtree
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.2.0'


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
    author_email='kuzmpvich.goog@gmail.com',
    license='MIT',
    url='https://github.com/kuzmoyev/Google-Calendar-Simple-API',
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "alabaster==0.7.12",
        "attrs==19.3.0",
        "Babel==2.6.0",
        "beautiful-date==1.0.1",
        "cachetools==3.0.0",
        "certifi==2018.11.29",
        "chardet==3.0.4",
        "docutils==0.14",
        "flake8==3.8.3",
        "google-api-python-client==1.7.7",
        "google-auth==1.6.2",
        "google-auth-httplib2==0.0.3",
        "google-auth-oauthlib==0.2.0",
        "httplib2==0.18.0",
        "idna==2.8",
        "imagesize==1.1.0",
        "importlib-metadata==1.6.1",
        "Jinja2==2.10.1",
        "MarkupSafe==1.1.0",
        "mccabe==0.6.1",
        "more-itertools==8.4.0",
        "oauthlib==3.0.1",
        "packaging==19.0",
        "pluggy==0.13.1",
        "py==1.8.1",
        "pyasn1==0.4.5",
        "pyasn1-modules==0.2.4",
        "pycodestyle==2.6.0",
        "pyflakes==2.2.0",
        "Pygments==2.3.1",
        "pyparsing==2.3.1",
        "pytest==5.4.3",
        "python-dateutil==2.7.2",
        "pytz==2018.9",
        "requests==2.22.0",
        "requests-oauthlib==1.2.0",
        "rsa==4.0",
        "six==1.11.0",
        "snowballstemmer==1.2.1",
        "Sphinx==1.8.3",
        "sphinxcontrib-websupport==1.1.0",
        "tzlocal==1.5.1",
        "uritemplate==3.0.0",
        "urllib3==1.25.3",
        "wcwidth==0.2.4"
    ],
    tests_require=[
        "pytest"
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
    ],
    cmdclass={
        'upload': UploadCommand,
        'build_sphinx': BuildDoc,
        'doctest': Doctest
    }
)
