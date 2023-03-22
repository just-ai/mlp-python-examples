#!/bin/bash

ACTION_NAME=composite-action-example

eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa
IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH_NAME
DOCKER_BUILDKIT=1 docker build . --ssh default -t $IMAGE

echo $IMAGE

docker push $IMAGE
