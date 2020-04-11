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

    (pyenv)$ python3 -m unittest discover -v

