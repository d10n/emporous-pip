#!/bin/bash

#set -x
printf '%s\n' '+ emporous build collection simple localhost:5000/demo/pyindex:latest --dsconfig dataset-config.yaml --plain-http' | pv -q --rate-limit=50

emporous build collection simple localhost:5000/demo/pyindex:latest --dsconfig dataset-config.yaml --plain-http
