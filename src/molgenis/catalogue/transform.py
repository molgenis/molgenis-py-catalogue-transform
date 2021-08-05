from zipfile import ZipFile
import os
import shutil
import pandas as pd
import numpy as np


def float_to_int(df):
    """
    Cast float64 Series to Int64.
    """
    for column in df.columns:
        if df[column].dtype == 'float64':
            df.loc[:, column] = df[column].astype('Int64')

    return df


class TransformData:
    """Transform data model of staging areas for Networks to data model in Data Catalogue"""

    def __init__(self, database, delete_from_filename, networks):
        self.path = './data/'
        self.database = database
        self.delete_from_filename = delete_from_filename
        self.networks = networks
        
        self.unzip_data()
        self.rename_and_delete_files()
        if self.delete_from_filename == 'Source':
            self.transform_cohort()
        if self.delete_from_filename == 'catalogue':
            self.back_to_staging()
        self.zip_data()

    def unzip_data(self):
        """Extract data.zip"""
        data = ZipFile('data.zip')
        try:
            data.extractall(self.path)
        except FileNotFoundError:
            print('Error: unzip failed')
            exit()
        except PermissionError:
            print('Error: unzip failed, permission denied')
            exit()
        try:
            os.remove("data.zip")
        except PermissionError:
            # remove fails on windows
            pass

    def rename_and_delete_files(self):
        for file_name in os.listdir(self.path):
            if file_name in ['molgenis.csv', 'molgenis_members.csv', 'molgenis_settings.csv', 'Networks.csv']:
                os.remove(self.path + file_name)
            elif self.delete_from_filename in file_name:
                new_file_name = file_name.replace(self.delete_from_filename, '')
                os.rename(self.path + file_name, self.path + new_file_name)

    def transform_cohort(self):
        df = pd.DataFrame()
        df.loc[0, 'acronym'] = self.database
        df.to_csv(self.path + 'Cohorts.csv', index=False)

        df = pd.DataFrame()
        df.loc[0, 'resource'] = self.database
        df.loc[0, 'version'] = '1.0.0'  # TODO: what to do about cohort versioning?
        df.to_csv(self.path + 'Releases.csv', index=False)

        for file_name in os.listdir(self.path):
            if file_name in ['CollectionEvents.csv', 'Subcohorts.csv']:
                try:
                    df = pd.read_csv(self.path + file_name)
                    df['resource'] = self.database
                    df = float_to_int(df)
                    df.to_csv(self.path + file_name, index=False)
                except pd.errors.EmptyDataError:
                    pass
            elif file_name in ['Tables.csv', 'Variables.csv', 'VariableValues.csv', 'RepeatedVariables.csv']:
                try:
                    df = pd.read_csv(self.path + file_name)
                    df['release.resource'] = self.database
                    df['release.version'] = '1.0.0' # TODO: what to do about cohort versioning?
                    df = float_to_int(df)
                    if file_name == 'VariableValues.csv':
                        df.loc[:, 'label'] = df['label'].replace(np.nan, 'NA')
                    df.to_csv(self.path + file_name, index=False)
                except pd.errors.EmptyDataError:
                    pass
            elif file_name in ['VariableMappings.csv', 'TableMappings.csv']:
                try:
                    df = pd.read_csv(self.path + file_name)
                    df['fromRelease.resource'] = self.database
                    df['fromRelease.version'] = '1.0.0'  # TODO: what to do about cohort versioning?
                    df['toRelease.resource'] = df['toNetwork']
                    df['toRelease.version'] = '1.0.0'  # TODO: fix versioning
                    df = float_to_int(df)
                    df.to_csv(self.path + file_name, index=False)
                except pd.errors.EmptyDataError:
                    pass

    def back_to_staging(self):
        for file_name in os.listdir(self.path):
            if file_name in ['Tables.csv', 'Variables.csv', 'VariableValues.csv', 'RepeatedVariables.csv']:
                try:
                    df = pd.read_csv(self.path + file_name)
                    df['network'] = df['release.resource']
                    df = df.loc[df['network'].isin(self.networks)]
                    df = float_to_int(df)
                    df.to_csv(self.path + file_name, index=False)
                except pd.errors.EmptyDataError:
                    pass

    def zip_data(self):
        """zip transformed data to upload.zip"""
        shutil.make_archive('upload', 'zip', self.path)
        # remove unzipped data
        shutil.rmtree(self.path)
