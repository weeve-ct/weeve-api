#!/bin/sh
VERSION=v0.7
TAG_NAME=gcr.io/$PROJECT_ID/$IMG_NAME:$VERSION
DOCKER_FOLDER=./docker

API_IMG_NAME=weeve-api
API_TAG_NAME=gcr.io/$PROJECT_ID/$API_IMG_NAME:latest
API_CONTAINER_NAME=some-$API_IMG_NAME

case "$1" in
  clean)
    if [[ ! -z $(docker images -f "dangling=true" -q) ]]
    then
      echo "Deleting dangling images"
      docker rmi $(docker images -f "dangling=true" -q)
    fi
    ;;

  build)
    echo "building image"
    docker build -t $API_IMG_NAME -f $DOCKER_FOLDER/server.dockerfile .
    echo "creating container"
    docker create -p 8080:8080 --name=$API_CONTAINER_NAME $API_IMG_NAME
    ;;

  cp)
    echo "copy dev config"
    docker cp ./local/server-config-dev.yaml some-weeve-api:/secrets/server-config.yaml
    ;;

  start)
    echo "starting container"
    docker start $API_CONTAINER_NAME
    ;;

  stop)
    echo "stopping container"
    docker stop $API_CONTAINER_NAME
    ;;

  kill)
    echo "deleting container"
    docker kill $API_CONTAINER_NAME
    docker rm $API_CONTAINER_NAME
    ;;

  delete)
    echo "deleting image"
    docker rmi $API_IMG_NAME
    ;;

  *)
    echo "Usage: "$1" {build|cp|start|stop|delete|clean}"
    exit 1
esac

exit 0
