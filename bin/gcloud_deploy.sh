#!/bin/bash

# Assumes you have gcloud properly authenticated and appengine-clean setup

# Steps:
# 1. Run test suite with tox
# 2. If tests ok:
#    a. Delete all but the last 5 version numbers
#    b. Deploy the app to google apps engine

tox
retVal=$?

if [ $retVal -eq 0 ]; then
    appengine-clean census-impute 5 --force
    gcloud app deploy app.yaml
else
    echo "Cancelling deployment since tox returned error code $retVal"
fi

exit $retVal