formtestautomation
==================

VLP Form Test Automation

To run, make sure the lastest version of Python is installed. 

Navigate into the folder in command line and run: 

python formtest.py

to run vlp form tests on urls in forms.csv and output to output.csv.

formtest also takes 4 or 2 parameters: 

python formtest.py (input file) (output file) (newsletter checked) (submit)

python formtest.py (newsletter checked) (submit)

Default is:
python formtest.py forms.csv output.csv False False