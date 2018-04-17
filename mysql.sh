#!/bin/sh
VERSION=v0.7
TAG_NAME=gcr.io/$PROJECT_ID/$IMG_NAME:$VERSION
DOCKER_FOLDER=./docker

DB_IMG_NAME=genie-db
DB_TAG_NAME=gcr.io/$PROJECT_ID/$API_IMG_NAME:latest
DB_CONTAINER_NAME=some-genie-db

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

  create)
    echo "creating container"
    docker create -p 3306:3306 --name=$DB_CONTAINER_NAME $DB_IMG_NAME
    ;;

  start)
    echo "starting container"
    docker start $DB_CONTAINER_NAME
    ;;

  stop)
    echo "stopping container"
    docker stop $DB_CONTAINER_NAME
    ;;

  delete)
    echo "deleting"
    docker rm $DB_CONTAINER_NAME
    ;;


  *)
    echo "Usage: "$1" {build|push}"
    exit 1
esac

exit 0
