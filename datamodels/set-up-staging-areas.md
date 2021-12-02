#Set up cohort staging areas as follows:

1. Go to a emx2 server

2. Load [CatalogueOntologies.zip](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/CatalogueOntologies.zip) 
in a schema called CatalogueOntologies (or choose another name, see 5). You should also load data in the tables, example data are 
[here](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/CatalogueOntologies_with_data.zip).

3. Load [catalogue_cdm.zip](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/catalogue_cdm.zip) in a schema called Catalogue 
(or choose another name, see 5). This database contains only the common data model variable metadata, which can be extracted from production 
data catalogue running the molgenis-py-catalogue-transform script.

4. Make separate schemas for each cohort that will enter data.

5. Optional: Change the schema references (column 'RefSchema') in molgenis.csv  
cohort_model.zip to the respective schema names used in 2 and 3. 

6. Load [cohort_model.zip](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/cohort_model.zip) to each cohort schema to 
create datamodel for cohort.

7. Cohort datamanagers can fill out Dictionary.xlsx and Mappings.xlsx templates. Documentation and links to templates are found 
[here](https://data-catalogue.molgeniscloud.org/apps/docs/#/cat_cohort-data-manager).


#Set up Network staging areas:

8. Make schema with name of network (e.g. LifeCycle)

9. Load [network_model.zip](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/network_model.zip)

10. Open Tables, add entry into table 'Networks' manually: acronym and 
name of network (note that acronym is capital sensitive!)

11. Central data managers of a network can fill out NetworkDictionary.xlsx. Documentation and links to templates are found 
[here](https://data-catalogue.molgeniscloud.org/apps/docs/#/cat_network-data-manager).
