# The Big IMDB quest

The application scrapes data from IMDB and adjusts IMDB ratings based on defined rules.

## Setup the python environment
- Tested python version 3.9
- Link for creating virtual envionments: https://docs.python.org/3.9/library/venv.html
- After the new virtual environment activation install the packages: `pip install -r requirements.txt`

## Run the application
The application can be run in the command line interface. After setting the working directory to the 
project folder then you can run the `run.py` in the following ways.

`python run.py`

`python run.py -l 20`  - Limit the movies to 20.

## Run unit tests:
For testing the functions please use the following line:

`python -m unittest discover -s tests`