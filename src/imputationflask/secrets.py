'''
imputationflask.secrets
-------------------
Gets secrets from google cloud secret manager. Relies on proper IAM

'''

from google.cloud import secretmanager

def csrf_key(config):

    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(config['PROJECT_NAME'], config['CSRF_KEY_SECRET_ID'], 'latest')
    response = client.access_secret_version(name)
    return response.payload.data.decode('UTF-8')
