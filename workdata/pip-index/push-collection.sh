#!/bin/bash

#set -x
printf '%s\n' '+ uor-client-go push --plain-http localhost:5000/demo/pyindex:latest' | pv -q --rate-limit=50

uor-client-go push --plain-http localhost:5000/demo/pyindex:latest
