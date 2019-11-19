# config.py global config

DEBUG = False  # Turns on debugging features in Flask

import os
SECRET_KEY = os.urandom(32)
FLASK_ENV = "prod"

PROJECT = 'census-impute'
TF_MODEL = 'base_census_infer'

BUCKET_ID = 'basic_census_binaries'
NUMERIC_MAPPER_PATH = 'numeric_mapper2.dill'
DATA_COLUMNS_PATH = 'data_columns.dill'
VAL2IND_PATH = 'val2ind.dill'
RECORD_DESCRIPTION_PATH = 'recordname2description2.dill'
PROJECT_NAME = 'census-impute'
