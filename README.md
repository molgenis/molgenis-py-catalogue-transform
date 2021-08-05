# About
This script is used to synchronize staging and production emx2 data catalogues. 
1. It extracts OntologyTerms from the staging area and loads them to the production catalogue. 
2. It extracts cohort variable metadata from emx2 staging databases, transforms the datamodel and loads the data to
to production catalogue.
3. It extracts network variable metadata from emx2 staging databases and loads them to the production catalogue.
4. It extracts the catalogue from production and loads the networks' (or models') variable metadata to the staging 
catalogue (containing only the common data models).

# System requirements
Python 3 (3.8.6)

create a virtual env 

pip install pandas==1.1.3
pip install numpy==1.19.2
pip install requests==2.21.0

# Set up details
Edit global variables (UPPER_CASE) in run.py to set up 
details for staging and production server.

# Run script
run.py


