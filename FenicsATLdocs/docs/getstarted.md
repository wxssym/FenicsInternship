# Library
The library is limited to internal use to analyse FENICS testing data for ATLAS TileCal upgrade Phase-II
## Download
you can download the library compressed files

* [``windows``](/library/FenicsATLlib.rar)

* [``linux``](/library/FenicsATLlib.tar)

Or download the git repository at 

* [``github.com/wxssym/FenicsATL``](https://github.com/wxssym/FenicsATL)

## Installation
The library can be installed by navigating to the FenicsATL folder where `setup.py` is located. And do a `pip install .` or `pip install -e .` for editable mode.

a verification after installation using ``pip list`` or `python3 -m FenicsATL --version
` is recommended.

## importation
You can simply import the library as :

        import FenicsATL as FATL