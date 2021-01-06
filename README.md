# triad-challenge
TRI-AD coding challenge

* To Run the app from the command line in the directory where LargestValues.py module is:
  * Make sure you have Python 3.8 installed.  To check `python --version` on command line. 
  * Create the virtual environment: `python -m venv env`
  * Install the required packages: `pip install -r requirements.txt`
  * `python LargestValues.py` for default options
  * `python LargestValues.py --help` for help on usage, shows how to set options
  * `python LargestValues.py --url https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt --x 5 --chunk_size 8` 

* Run the pytest on the app from the command line in the directory where LargestValues.py module is:
  * `pytest`
  * `pytest -v` for more verbose output


* Build the Dockerized app:
  * Make sure you have docker installed. To check `docker --version`
  * From the root directory of the app, run the following:
    * `docker build --rm -f Dockerfile -t triadchallenge:latest .`

* Run the app inside the docker container 
  * Run default configuration `docker run --rm -it triadchallenge:latest` 
  * `python LargestValues.py --help` for help on usage, shows how to set options
  * Run with options `docker run --rm -it triadchallenge:latest --url https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt --x 5 --chunk_size 8` 

* Run the pytests inside docker container
  * `docker run --rm -it --entrypoint "pytest" triadchallenge:latest /app`

* Heapsort used in the priority queue is not stable.  So if we are returning 1 top record and two records have the same number values, then keys to either can be returned.  But since in the requirements output does not need to be in any particular order both answers should be correct. 

