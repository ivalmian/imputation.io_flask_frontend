# load_binaries.py
# Reads binaries for the ml model using paths in app.config and returns them

# Binaries saved with dill
import dill


def load_binaries(app):

    with open(app.config['NUMERIC_MAPPER_PATH'], 'rb') as fin:
        numeric_mappers = dill.load(fin)
    with open(app.config['DATA_COLUMNS_PATH'], 'rb') as fin:
        data_columns = dill.load(fin)
    with open(app.config['VAL2IND_PATH'], 'rb') as fin:
        val2ind = dill.load(fin)
    with open(app.config['RECORD_DESCRIPTION_PATH'], 'rb') as fin:
        recordname2description = dill.load(fin)

    return {'numeric_mappers': numeric_mappers,
            'data_columns': data_columns,
            'val2ind': val2ind,
            'recordname2description': recordname2description}
