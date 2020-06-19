#!/bin/bash


export GOOGLE_APPLICATION_CREDENTIALS="../gcloud_credential/census-impute-d47bc435f1d0.json"
gunicorn --chdir src "imputationflask:application()" -b :5000