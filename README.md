Nested Dictionary of Dictionaries of Arrays
=======================

Given an input as json array (each element is a flat dictionary), parses this json, and return a nested dictionary of dictionaries of arrays, with keys specified in command line arguments and the leaf values as arrays of flat dictionaries.

E.g. 
    cat ../docs/input.json | python json_parser.py key_level_1 key_level_2 key_level_3

# Setup

1 - Install dev prereqs (use equivalent linux or windows pkg mgmt)
----

    brew install python3.6
    brew install virtualenv


2 - Set up a Python virtual environment (from project root directory)
----

    make venv
    source venv/bin/activate


3 - Install required python packages into the virtual env
----
    make init


4 - Run the tests from project root directory
----
    . scripts/code-coverage.sh


5 - Run the code
----
    python 
