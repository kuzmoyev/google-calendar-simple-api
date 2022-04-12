# Contributing to GCSA

Welcome and thank you for considering contributing to *Google Calendar Simple API* open source project!

Before contributing to this repository, please first discuss the change you wish to make via 
[Issue](https://github.com/kuzmoyev/google-calendar-simple-api/issues), 
[GitHub Discussion](https://github.com/kuzmoyev/google-calendar-simple-api/discussions), or [Discord](https://discord.gg/mRAegbwYKS).

## Steps to contribute changes

1. Fork the repository
2. Clone it with `git clone git@github.com:{your_username}/google-calendar-simple-api.git`
3. Install dependencies if needed with `pip install -e .` (or `pip install -e ".[dev]"` if you want to run tests, compile documentation, etc.). 
Use [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid polluting your global python
4. Make and commit the changes. Add `closes #{issue_number}` to commit message if applies
5. Run the tests with `tox` (these will be run on pull request):
    * `tox` - all the tests
    * `tox pytest` - unit tests
    * `tox flake8` - style check
    * `tox sphinx` - docs compilation test
6. Push
7. Create pull request
    * towards `dev` branch if the changes require a new GCSA version (i.e. changes in [gcsa](https://github.com/kuzmoyev/google-calendar-simple-api/tree/master/gcsa) module)
    * towards `master` branch if they don't (e.x. changes in README, docs, tests)

## While contributing

* Follow the [Code of conduct](https://github.com/kuzmoyev/google-calendar-simple-api/blob/master/.github/CODE_OF_CONDUCT.md)
* Follow the code style of the projects (that includes [pep8](https://peps.python.org/pep-0008/))
* If needed (use your best judgement):
    * Add documentation of your changes to code and/or to [read-the-docs](https://github.com/kuzmoyev/google-calendar-simple-api/tree/master/docs/source)
    * Add [tests](https://github.com/kuzmoyev/google-calendar-simple-api/tree/master/tests)
