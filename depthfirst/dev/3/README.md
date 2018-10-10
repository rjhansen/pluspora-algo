# Helpful Tools

## Editors

Nearly any programmer's text editor will do; many have excellent support for Python.  I personally use Visual Studio Code, a crossplatform programmer's editor by Microsoft.

## Linters

* [pylint](https://www.pylint.org/) is one of the best free linters for Python code.  It's available in the repositories of many Linux distros: `sudo apt install pylint3` is the magic Ubuntu invocation.

## Conformance tools

* [pep8](https://pypi.org/project/pep8/) is the Python community's standard tool for formatting code the Python way. `sudo apt install pep8` is your key to the conformance checker.  Your first few programs will get murdered by `pep8`, but after a while you'll find yourself writing code the Python way.
* [autopep8](https://pypi.org/project/autopep8/).  Where `pep8` will tell you about conformance problems, `autopep8` attempts to fix them for you.  It's not in the Ubuntu repos, though: I installed it by `sudo -H python3 -m pip install autopep8`.

## Documentation

* [Sphinx](http://www.sphinx-doc.org/en/master/).  The Python community has standardized on Sphinx for its module documentation.  Once we develop our depth-first searcher into a usable tool that might warrant re-use, we'll use Sphinx to give it the kind of API reference programmers hope for.  On Ubuntu, `sudo apt install python3-sphinx` will get you started.
* `pyreverse`, shipped with Pylint, can inhale absurdly complicated Python scripts and output lovely UML diagrams.  It's worth keeping under your hat if you ever get mugged by someone's object-oriented monstrosity and need a high-level view of it.
