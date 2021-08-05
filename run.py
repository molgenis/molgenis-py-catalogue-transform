from src.molgenis.catalogue.main import Molgenis
from src.molgenis.catalogue.transform import TransformData

NETWORKS = ['LifeCycle', 'ATHLETE', 'LongITools']  # fill out network databases in staging
COHORTS = ['NFBC1966', 'NFBC1986', 'KANC']  # fill out cohort databases in staging

# Staging server details
URL_STAGING = 'https://data-catalogue-staging.molgeniscloud.org/'  # fill out url of staging area
USERNAME_STAGING = 'admin'
PASSWORD_STAGING = ''

# Production server details
URL_PROD = 'https://emx2.test.molgenis.org/'  # fill out url of combined production catalogue
USERNAME_PROD = 'admin'
PASSWORD_PROD = ''

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

