#Set up cohort staging areas as follows:

1. Go to an emx2 server

2. Load [CatalogueOntologies.zip](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/CatalogueOntologies.zip) 
in a schema called CatalogueOntologies (or choose another name, see 5). You should also load data in the tables, example data are 
[here](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/CatalogueOntologies_with_data.zip).

3. Load [CommonDataModels.csv](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/catalogue_cdm.csv) in a schema called Catalogue 
(or choose another name, see 5). This database contains only the common data model variable metadata, which can be extracted from production 
data catalogue running the molgenis-py-catalogue-transform script.

4. Make separate schemas for each cohort that will enter data. At least cohort pid and name should already be filled out in production 'catalogue' schema
table 'Cohorts'.

5. Optional: Change the schema references (column 'RefSchema') in molgenis.csv  
cohort_model.csv to the respective schema names used in 2 and 3. 

6. Load [cohort_model.csv](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/cohort_model.csv) to each cohort schema to 
create datamodel for cohort.

7. Cohort datamanagers can fill out Dictionary.xlsx and Mappings.xlsx templates. Documentation and links to templates are found 
[here](https://data-catalogue.molgeniscloud.org/apps/docs/#/cat_cohort-data-manager).


#Set up Network common data model staging areas:

8. Make schema with name of model, corresponging to the name it has in data-catalogue.molgeniscloud.org (e.g. LifeCycle_CDM)

9. Load [network_model.csv](https://github.com/molgenis/molgenis-py-catalogue-transform/datamodels/network_model.csv)

10. Open Tables, add entry into table 'Models' manually: pid and 
name of model

11. Central data managers of a network can fill out NetworkDictionary.xlsx. Documentation and links to templates are found 
[here](https://data-catalogue.molgeniscloud.org/apps/docs/#/cat_network-data-manager).
