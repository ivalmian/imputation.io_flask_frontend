# load_binaries.py
# Reads binaries for the ml model using paths in app.config and returns them

# Binaries saved with dill

import dill
import numpy as np


def load_binaries(config):

    if config['FLASK_ENV'] == 'dev': 
        with open(config['NUMERIC_MAPPER_PATH'], 'rb') as fin:
            numeric_mappers = dill.load(fin)
        with open(config['DATA_COLUMNS_PATH'], 'rb') as fin:
            data_columns = dill.load(fin)
        with open(config['VAL2IND_PATH'], 'rb') as fin:
            val2ind = dill.load(fin)
        with open(config['RECORD_DESCRIPTION_PATH'], 'rb') as fin:
            recordname2description = dill.load(fin)

    elif config['FLASK_ENV'] == 'prod': #pragma: no cover

        from google.cloud import storage

        bucket = storage.Client(project=config['PROJECT_NAME']).get_bucket(config['BUCKET_ID'])
        numeric_mappers = dill.loads(bucket.blob(config['NUMERIC_MAPPER_PATH']).download_as_string())
        data_columns = dill.loads(bucket.blob(config['DATA_COLUMNS_PATH']).download_as_string())
        val2ind = dill.loads(bucket.blob(config['VAL2IND_PATH']).download_as_string())
        recordname2description = dill.loads(bucket.blob(config['RECORD_DESCRIPTION_PATH']).download_as_string())

    else:
        raise ValueError(f'FLASK_ENV is set to unsupported {config["FLASK_ENV"]}')

    return {'numeric_mappers': numeric_mappers,
            'data_columns': data_columns,
            'val2ind': val2ind,
            'recordname2description': recordname2description}
