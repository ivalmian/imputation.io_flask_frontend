# config.py global config

DEBUG = False  # Turns on debugging features in Flask

# import os
SECRET_KEY = b'daae7948824525c1b8b59f9d5a75e9c0404e46259c7b1e17a4654a7e73c91b87'
FLASK_ENV = "prod"

PROJECT = 'census-impute'
TF_MODEL = 'base_census_infer'

BUCKET_ID = 'basic_census_binaries'
NUMERIC_MAPPER_PATH = 'numeric_mapper2.dill'
DATA_COLUMNS_PATH = 'data_columns.dill'
VAL2IND_PATH = 'val2ind.dill'
RECORD_DESCRIPTION_PATH = 'recordname2description2.dill'
PROJECT_NAME = 'census-impute'
