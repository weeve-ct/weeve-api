#!/bin/sh
PROJECT_ID="$(gcloud config get-value project --quiet)"
VERSION=latest
DOCKER_FOLDER=./docker

API_IMG_NAME=weeve-api
API_VERSION=latest
API_TAG_NAME=gcr.io/$PROJECT_ID/$API_IMG_NAME:$API_VERSION
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

  push)
    echo "pushing"
    docker tag $API_IMG_NAME $API_TAG_NAME
    gcloud docker -- push $API_TAG_NAME
    docker rmi $API_TAG_NAME
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
