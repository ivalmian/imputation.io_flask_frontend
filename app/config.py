'''
app.config
-------------------
Prod config, can be overwritten by instance/config.py when present

'''

# non-instance config is for prod
FLASK_ENV = "prod"
DEBUG = False 

# google stuff
PROJECT_NAME = 'census-impute'
TF_MODEL = 'base_census_infer'
CSRF_KEY_SECRET_ID = 'csrf-key'

# binaries
BUCKET_ID = 'basic_census_binaries'
NUMERIC_MAPPER_PATH = 'numeric_mapper3.dill'
DATA_COLUMNS_PATH = 'data_columns.dill'
VAL2IND_PATH = 'val2ind.dill'
RECORD_DESCRIPTION_PATH = 'recordname2description2.dill'


# sql 
SQLALCHEMY_TRACK_MODIFICATIONS = False