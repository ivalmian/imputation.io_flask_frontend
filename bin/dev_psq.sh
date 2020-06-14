#!/bin/bash

docker run --name imputation_db -e POSTGRES_PASSWORD=imp -d -p 5432:5432  postgres