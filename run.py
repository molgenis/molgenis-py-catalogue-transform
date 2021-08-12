from posixpath import join
from src.molgenis.catalogue.main import Molgenis
from src.molgenis.catalogue.transform import TransformData
from decouple import config

NETWORKS = config('MG_CATALOGUE_NETWORKS', cast=lambda v: [s.strip() for s in v.split(',')])
COHORTS = config('MG_CATALOGUE_COHORTS', cast=lambda v: [s.strip() for s in v.split(',')])  

# Staging server details
URL_STAGING = config('MG_CATALOGUE_URL_STAGING')
USERNAME_STAGING = config('MG_CATALOGUE_USERNAME_STAGING')
PASSWORD_STAGING = config('MG_CATALOGUE_PASSWORD_STAGING')

# Production server details
URL_PROD = config('MG_CATALOGUE_URL_PROD')
USERNAME_PROD = config('MG_CATALOGUE_USERNAME_PROD')
PASSWORD_PROD = config('MG_CATALOGUE_PASSWORD_PROD')

print('-----  Config variables loaded ----')

print('URL_STAGING: ' + URL_STAGING)
print('USERNAME_STAGING: ' + USERNAME_STAGING)
print('PASSWORD_STAGING: ******')

print('URL_PROD: ' + URL_PROD)
print('USERNAME_PROD: ' + USERNAME_PROD)
print('PASSWORD_PROD: *****' )

print('NETWORKS: ' + ', '.join(NETWORKS))
print('COHORTS: ' + ', '.join(COHORTS))

print('-----   ----')


# CatalogueOntologies ETL
# sign in to staging server
print('Sign in to staging server.')
session_staging = Molgenis(
    url=URL_STAGING,
    database='CatalogueOntologies',
    email=USERNAME_STAGING,
    password=PASSWORD_STAGING
)
# extract data
print('Extract data (data.zip)')
session_staging.downloadZip()

# transform data
print('Transform data, database: %s, delete_from_filename: %s' % ('CatalogueOntologies', 'Ontologies'))
transform_ontologies = TransformData('', 'Ontologies', NETWORKS)

# sign in to production server
print('Sign in to production server.')
session_prod = Molgenis(
    url=URL_PROD,
    database='catalogue',
    email=USERNAME_PROD,
    password=PASSWORD_PROD
)
# load data
print('Load data (upload.zip)')
session_prod.uploadZip()

# Networks ETL
print()
print('Network ETL')
for item in NETWORKS:
    # sign in to staging server
    print('Sign in to staging server for database: %s.' % (item))
    session_staging = Molgenis(
        url=URL_STAGING,
        database=item,
        email=USERNAME_STAGING,
        password=PASSWORD_STAGING
    )
    # extract data
    print('Extract data (data.zip)')
    session_staging.downloadZip()
    # transform data

    print('Transform data, database: %s, delete_from_filename: %s' % (item, 'Target'))
    transform_network = TransformData(item, 'Target', NETWORKS)
    # log in to test server
    # print('Sign in to test server.')
    # session_prod = Molgenis(
    #     url=URL_PROD,
    #     database='catalogue',
    #     email=USERNAME_PROD,
    #     password=PASSWORD_PROD
    # )
    # load data
    print('Load data (upload.zip)')
    session_prod.uploadZip()

# Cohorts ETL
print()
print('Cohorts ETL')
for item in COHORTS:
    # sign in to staging server
    print('Sign in to staging server for database: %s.' % (item))
    session_staging = Molgenis(
        url=URL_STAGING,
        database=item,
        email=USERNAME_STAGING,
        password=PASSWORD_STAGING
    )
    # extract data
    print('Extract data (data.zip)')
    session_staging.downloadZip()
    # transform data
    print('Transform data, database: %s, delete_from_filename: %s' % (item, 'Source'))
    transform_cohorts = TransformData(item, 'Source', NETWORKS)
    # log in to test server
    # print('Sign in to production server.')
    # session_prod = Molgenis(
    #     url=URL_PROD,
    #     database='catalogue',
    #     email=USERNAME_PROD,
    #     password=PASSWORD_PROD
    # )
    # load data
    print('Load data (upload.zip)')
    session_prod.uploadZip()

# Networks to staging catalogue ETL
print()
print('Networks to staging catalogue ETL')
# log in to production server
print('Sign in to test server for database: catalogue.')
session_prod = Molgenis(
    url=URL_PROD,
    database='catalogue',
    email=USERNAME_PROD,
    password=PASSWORD_PROD
)
# extract data
print('Extract data (data.zip)')
session_prod.downloadZip()
# transform data
print('Transform Networks data, database: %s,  delete_from_filename: %s' % ('catalogue', 'catalogue'))
back_to_staging = TransformData('', 'catalogue', NETWORKS)
# log in to staging server
print('Sign in to staging server for database: Catalogue.')
session_staging = Molgenis(
    url=URL_STAGING,
    database='Catalogue',
    email=USERNAME_STAGING,
    password=PASSWORD_STAGING
)
# load data
print('Load data (upload.zip)')
session_staging.uploadZip()

