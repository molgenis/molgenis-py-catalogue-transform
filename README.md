# About
This script is used to synchronize staging area and data catalogues. 
1. It extracts OntologyTerms from the staging area and loads them to the catalogue. 
2. It extracts cohort variable metadata from staging area, transforms the data model and loads the data to
the catalogue.
3. It extracts network variable metadata from staging areas and loads them to the catalogue.
4. It extracts all data from the catalogue and loads the networks' (or models') variable metadata to the staging 
area catalogue (containing only the common data models).

See folder docs for more details on data flows.
See datamodels for explanation how to set up staging areas and the datamodels to use in the databases.

# System requirements
- Python 3 (3.8.6)

- Git

# Initial one-time setup for running the transform script

Use virtual env to get a consistent python environment.

1. Clone the github repository

`git clone git@github.com:molgenis/molgenis-py-catalogue-transform.git`

`cd molgenis-py-catalogue-transform`

2. Create a virtual python environment

`python -m venv venv` 

3. Activate the virtual python environment

`source venv/bin/activate`

4. Install the script dependencies from requirements.txt file

`pip install -r requirements.txt`

More info see:

mac: https://www.youtube.com/watch?v=Kg1Yvry_Ydk

windows: https://www.youtube.com/watch?v=APOPm01BVrk

# Running the script
## Using docker 

(Optionally build the image)

`docker build -t molgenis/molgenis-py-catalogue-transform:latest .`

Run the script ( and remove container when done)

`docker run --rm -it  molgenis/molgenis-py-catalogue-transform:latest`

## Using docker-compose  

Edit the env setting in the docker-compose.yml as needed

`docker-compose up`

## Using the python virtual environment
1. Activate the virtual python environment

`source venv/bin/activate`

(1.1 Optionally update the requirements)

`pip install -r requirements.txt`

(1.2 Optionally configure the script by setting the environment variables)

can be done by adding a .env file and filling out the values ( see .env-example as a template)
or directly setting the values on the system environment.
 
| Name        | description  |
| ------------- | ------------- |
| MG_CATALOGUE_NETWORKS | comma separated list of network names|
| MG_CATALOGUE_COHORTS | comma separated list of network names |
| MG_CATALOGUE_URL_STAGING| full url of staging server|
| MG_CATALOGUE_USERNAME_STAGING| |
| MG_CATALOGUE_PASSWORD_STAGING| |
| MG_CATALOGUE_URL_PROD| full url of production server |
| MG_CATALOGUE_USERNAME_PROD| |
| MG_CATALOGUE_PASSWORD_PROD| |

2. Run the script

`python run.py`

3. deactivate the the virtual python environment

`deactivate`

# For script developers
Make sure to update the requirements.txt file if requirements change (added, removed, version change ...)

Git project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to trigger releases and version updates if needed.
Make sure to use [appropriate commit message format](https://www.conventionalcommits.org/en/v1.0.0/#specification)


