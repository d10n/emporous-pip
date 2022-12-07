#!/bin/bash

#set -x
printf '%s\n' '+ uor-client-go build collection simple localhost:5000/demo/pyindex:latest --dsconfig dataset-config.yaml --plain-http' | pv -q --rate-limit=50

uor-client-go build collection simple localhost:5000/demo/pyindex:latest --dsconfig dataset-config.yaml --plain-http
