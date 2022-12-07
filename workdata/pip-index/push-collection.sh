#!/bin/bash

set -x

uor-client-go push --plain-http localhost:5000/demo/pyindex:latest
