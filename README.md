# VIX Futures Databridge

The purpose of the project is to create a process that gathers on a daily basis **volatility** futures data and produces historical time series that can be used as raw data to train the volatility strategy models.


requirements.txt contains the libraries used in the venv.


## Setup

These instructions assume you've already installed a version of Python 3.

1. Run pip3 to install vitualenv:

    `pip3 install virtualenv`

1. You'll need the full path to the Python 3 version of virtualenv, so run the following to view it:

    `which virtualenv`
    >/home/username/opt/python-3.6.2/bin/virtualenv

1. Make a note of the full file path to the custom version of Python you just installed:

    `which python3`
    >/home/username/opt/python-3.6.2/bin/python

1. Navigate to your selected directory, where you'll create the new virtual environment:

    `cd ~/example.com`

1. Create the virtual environment while you specify the version of Python you wish to use. The following command creates a virtualenv named 'my_project' and uses the -p flag to specify the full path to the Python3 version you just installed: 

    `virtualenv -p /home/example_username/opt/python-3.6.2/bin/python3 my_project`

    >Running virtualenv with interpreter /home/example_username/opt/python-3.6.2/bin/python3
    >Using base prefix '/home/example_username/opt/python-3.6.2'
    >New python executable in /home/example_username/example.com/env/bin/python3
    >Also creating executable in /home/example_username/example.com/env/bin/python
    >Installing setuptools, pip, wheel...done.


## Usage

1. To activate the new virtual environment, run the following: 

    `source my_project/bin/activate`

     The name of the current virtual environment appears to the left of the prompt. For example: 

     >(my_project) [server]$ 

1. To verify the correct Python version, run the following: 

    `python -V`

    >Python 3.6.2

1. Install the required libraries

    `pip install pandas`

    `pip install pandas-market-calendars`

    `pip install QuantLib-Python`

    `pip install matplotlib`


### Deactivating your virtualenv

* When finished working in the virtual environment, you can deactivate it by running the following:

    `deactivate`

Virtual environment instructions source:

https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3


## Code Structure

Code runs in the following order:

1. top_script.py

1. vix_futures_exp_dates.py
1. download_link.py
1. compare_files.py
1. time_series.py

    **or**

1. weigted_time_series.py
