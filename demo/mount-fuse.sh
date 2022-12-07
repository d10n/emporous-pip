#!/bin/bash

#set -x
printf '%s\n' '+ uor-fuse-go mount --plain-http localhost:5000/demo/pyindex:latest /mnt' | pv -q --rate-limit=50

uor-fuse-go mount --plain-http localhost:5000/demo/pyindex:latest /mnt
