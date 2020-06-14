#!/bin/bash

# Depends on:
# 1. Docker
# 2. PSQL client
# 3. postgres docker image


old_container=$(docker ps -a -q --filter name="dev")

if [[ -n $old_container ]]; then
    echo "stopping old container"
    docker stop $old_container
    echo "removing old container"
    docker rm $old_container
else
    echo "no old container detected"
fi 

echo "Running new container"

export PGPASSWORD="imp"

docker run --name dev -e POSTGRES_PASSWORD=$PGPASSWORD -d -p 5432:5432  postgres

retVal=$?

if [ $retVal -eq 0 ]; then
    
    echo "Password was set to $PGPASSWORD"
    DBNAME="imputation"
    echo "Creating DB name=$DBNAME"

    #TODO: figure out why passing $PGPASSWORD via export doesn't work 
    createdb -h 127.0.0.1 -p 5432 -U postgres $DBNAME -W
else
    echo "Docker returned error code $retVal"
fi


