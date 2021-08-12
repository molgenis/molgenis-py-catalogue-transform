# About
This script is used to synchronize staging area and data catalogues. 
1. It extracts OntologyTerms from the staging area and loads them to the catalogue. 
2. It extracts cohort variable metadata from staging area, transforms the datamodel and loads the data to
to catalogue.
3. It extracts network variable metadata from staging area and loads them to the catalogue.
4. It extracts the model from catalogues and loads the networks' (or models') variable metadata to the staging 
area (containing only the common data models).

# System requirements
- Python 3 (3.8.6)

- Git

# Initial one-time setup for running the transform script

Use virtual env to get a consistent python environment.
Initially you need to set up the virtual python environment.

1. Clone the github repository

`git clone git@github.com:molgenis/molgenis-py-catalogue-transform.git`

`cd molgenis-py-catalogue-transform.git`

2. Create a virtual python environment

`python -m venv venv` 

3. Activate the virtual python environment

`source venv/bin/activate`

4. Install the script dependencies from requirements.txt file

`pip install -r requirements.txt`

More info see:

mac: https://www.youtube.com/watch?v=Kg1Yvry_Ydk

window: https://www.youtube.com/watch?v=APOPm01BVrk

# Running the script using the virtual python virtual environment
1. Activate the virtual python environment

`source venv/bin/activate`

(1.1 Optionally update the requirements)

`pip install -r requirements.txt`

(1.2 Optionally configure the script by setting the environment variables)

can be done by adding a .env file and filling out the values ( see .env-example als a template)
or directly setting the values on the system environment.
 
| Name        | description  |
| ------------- | ------------- |
| MG_CATALOGUE_NETWORKS | comma separated list of network names|
| MG_CATALOGUE_COHORTS | comma separated list of network names |
| MG_CATALOGUE_URL_STAGING| full url of stating server|
| MG_CATALOGUE_USERNAME_STAGING|  |
| MG_CATALOGUE_PASSWORD_STAGING| |
| MG_CATALOGUE_URL_PROD| full url of stating server |
| MG_CATALOGUE_USERNAME_PROD| |
| MG_CATALOGUE_PASSWORD_PROD| |

2. Run the script

`python run.py`

3. deactivate the the virtual python environment

`deactivate`

# For script developers
Make sure to update the requirements.txt file is requirements change ( added , removed, version change ...)


