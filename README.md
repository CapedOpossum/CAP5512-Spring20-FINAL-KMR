# CAP 5512: Evolutionary Computation Spring 2020 Final Project

## Team Members

* Kyle Benko
* Matthew Kurtz
* Rolando Nieves

## Development Environment

Create virtual Python 3 environment using the included `requirements.txt` file:

    $ python3 -m venv pyenv
    ...
    $ . pyenv/bin/activate
    (pyenv) $ pip3 install -r ./requirements.txt
    ...

## Unit Tests

Unit tests have been written for some of the project's components. They can be
run via the Python 3 `unittest` module auto-discovery facility (when run from
the project root directory under the project's virtual environment; see
*Development Environment*):

    (pyenv) $ python3 -m unittest discover -v

## Run One-Max

Part of the validation of the DEAP package included evaluating the ease and
feasibility with which OneMax could be implemented on it. DEAP does not include
configuration file declarative facilities like the CAP 5512 Java-based code
base. The `gabasic` package is the first attempt at adding such a facility.
OneMax can be run as follows:

    (pyenv) $ python3 -m gabasic one_max.ini

## Run Tic-Tac-Toe

The repository contains a baseline configuration file that is able to use the
`gabasic` package to find an optimal Tic-Tac-Toe player policy. To execute the
search, run:

    (pyenv) $ python3 -m gabasic tic_tac_toe.ini
