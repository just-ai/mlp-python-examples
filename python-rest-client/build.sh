#!/bin/bash

ROOT=$(dirname $0)
cd "$ROOT"

if ! [[ -z "$1" ]]
then
    BRANCH=$(echo $1 | tr '[:upper:]' '[:lower:]')
else
    BRANCH=$(git rev-parse --abbrev-ref HEAD | tr '[:upper:]' '[:lower:]')
fi

ACTION_NAME=rest_client_example
IMAGE=docker-pub.caila.io/caila-public/$ACTION_NAME:$BRANCH

# using static LTS version of SDK
# ./set_mlp_sdk_version.sh "$BRANCH"

DOCKER_BUILDKIT=1 docker build . -t "$IMAGE"

echo "$IMAGE"

docker push "$IMAGE"
