#!/bin/bash

# ./demo/build-demo.sh demo/Dockerfile epip-demo

set -x

poetry install
poetry build
cp dist/* demo/dist/

run_cmd="$(command -pv podman || command -pv docker)"
DOCKER_BUILDKIT=1 "$run_cmd" build . -f "$1" -t "$2"
