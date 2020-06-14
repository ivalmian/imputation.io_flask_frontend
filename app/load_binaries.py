'''
app.load_binaries
-------------------
Reads binaries for the ml model using paths in app.config and returns them

Binaries saved with dill
'''

import dill
import numpy as np
from google.cloud import storage

def load_binaries(config):

    bucket = storage.Client(project=config['PROJECT_NAME']).get_bucket(config['BUCKET_ID'])
    numeric_mappers = dill.loads(bucket.blob(config['NUMERIC_MAPPER_PATH']).download_as_string())
    data_columns = dill.loads(bucket.blob(config['DATA_COLUMNS_PATH']).download_as_string())
    val2ind = dill.loads(bucket.blob(config['VAL2IND_PATH']).download_as_string())
    recordname2description = dill.loads(bucket.blob(config['RECORD_DESCRIPTION_PATH']).download_as_string())
 
    return {'numeric_mappers': numeric_mappers,
            'data_columns': data_columns,
            'val2ind': val2ind,
            'recordname2description': recordname2description}
