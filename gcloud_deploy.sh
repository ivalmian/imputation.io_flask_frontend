#!/bin/bash

#assumes you have gcloud properly authenticated and appengine-clean setup

appengine-clean census-impute 5 --force
gcloud app deploy app.yaml