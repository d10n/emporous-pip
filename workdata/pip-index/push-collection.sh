#!/bin/bash

#set -x
printf '%s\n' '+ emporous push --plain-http localhost:5000/demo/pyindex:latest' | pv -q --rate-limit=50

emporous push --plain-http localhost:5000/demo/pyindex:latest
