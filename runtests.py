#!/usr/bin/env python
import sys
import subprocess
import pytest


FLAKE8_ARGS = ['scout', 'tests/', '--ignore=E501' ]
PYTEST_ARGS = [ '--cov=scout', '--tb=short', '-rw' ]


def exit_on_failure(command, message=None):
    if command:
        sys.exit(command)


def flake8_main(args):
    print('Running: flake8', FLAKE8_ARGS)
    command = subprocess.call(['flake8'] + args)
    print("" if command else "Success. flake8 passed.")
    return command


def run_tests_coverage():
    if __name__ == "__main__":
        pytest.main(PYTEST_ARGS)

exit_on_failure(run_tests_coverage())
#exit_on_failure(flake8_main(FLAKE8_ARGS))
