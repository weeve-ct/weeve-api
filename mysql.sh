#!/bin/sh
IMG_NAME=sugah_dadeez_api


#!/bin/sh

IMG_NAME=funnel-api
VERSION=v0.7
TAG_NAME=gcr.io/$PROJECT_ID/$IMG_NAME:$VERSION
DOCKER_FOLDER=./docker

DB_IMG_NAME=genie-db
DB_TAG_NAME=gcr.io/$PROJECT_ID/$API_IMG_NAME:latest

case "$1" in
  build)
    echo "building"
    docker build -t $DB_IMG_NAME -f $DOCKER_FOLDER/local_mysql.dockerfile .

    if [[ ! -z $(docker images -f "dangling=true" -q) ]]
    then
      echo "Deleting dangling images"
      docker rmi $(docker images -f "dangling=true" -q)
    fi
    ;;

  clean)
    docker kill $(docker ps -aq)
    docker rm $(docker ps -aq)

    if [[ ! -z $(docker images -f "dangling=true" -q) ]]
    then
      echo "Deleting dangling images"
      docker rmi $(docker images -f "dangling=true" -q)
    fi
    ;;

  start)
    echo "starting"
    docker run --detach --name=genie-db -p 3306:3306 $DB_IMG_NAME
    ;;

  stop)
    echo "stopping"
    docker kill genie-db
    docker rm genie-db
    ;;


  *)
    echo "Usage: "$1" {build|push}"
    exit 1
esac

exit 0
