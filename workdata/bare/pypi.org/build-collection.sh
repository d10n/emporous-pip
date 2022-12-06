#!/bin/bash

set -x

uor build collection simple localhost:5000/demo/pyindex:latest --dsconfig dataset-config.yaml --plain-http
