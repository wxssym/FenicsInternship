# Welcome to FenicsATL documentation
a FENICS data analysis Python library (Python 3.6+) with a multipurpose graphical tools with filtering. Part of the **"Analysis of FENICS ageing data, for ATLAS upgrade"**, at the Laboratoire de Physique de Clermont **LPC**.

## Modules
FenicsATL functions are separated into different modules that achieve :  

* [`FenicsATL.FenStruct`](FenStruct#FenStruct-module) - module with functions that parse/read/save the FENICS boards data in a pandas dataframe, and inside a one single json file.
* [`FenicsATL.FenLoad`](FenLoad#FenLoad-module) -  module with  functions that load filter the saved FENICS data, and separates Slow/Fast dataframes.
* [`FenicsATL.FenGraphs`](FenGraphs#FenGraphs-module) -  module with functions that Plot using `Matplotlib` and `Bokeh` the different features of FENICS boards.
* [`FenicsATL.FenUtils`](FenUtils#FenUtils-module) -  module with utility functions that handles io, `SSH` connections, `MySQL` database connections.

## Dependencies
FenicsATL package need these Python modules installed to properly work

** scientific  python libraries**

 - [`numpy`](https://numpy.org/install/) scientific computing in Python.
 - [`pandas`](https://pandas.pydata.org/) easy-to-use data structures and data analysis tools for the Python programming language.
 - [`scipy`](https://scipy.org/install/) is an open-source software for mathematics, science, and engineering..
 - [`scikit learn`](https://scikit-learn.org/stable/install.html) is an open source machine learning library that supports supervised and unsupervised learning.

** graphical python libraries**

 - [`Bokeh`](https://docs.bokeh.org/en/latest/docs/first_steps.html#first-steps) Bokeh is a Python library for creating interactive visualizations for modern web browsers..
 - [`pyplot.matplotlib`](https://matplotlib.org/stable/index.html)  is a state-based interface to matplotlib. It provides an implicit, MATLAB-like, way of plotting.

** io/socket python libraries**

 - [`paramiko`](https://www.paramiko.org/installing.html) is a pure-Python 1 (3.6+) implementation of the SSHv2 protocol.
 - [`mysql.connector`](https://dev.mysql.com/doc/connector-python/en/) a self-contained Python driver for communicating with MySQL servers.
