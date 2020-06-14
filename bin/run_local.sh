#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="gcloud_credential/census-impute-d47bc435f1d0.json"
gunicorn app:app -b :5000