#!/bin/bash

#set -x
printf '%s\n' '+ emporous-fuse-go mount --plain-http localhost:5000/demo/pyindex:latest /mnt' | pv -q --rate-limit=50

emporous-fuse mount --plain-http localhost:5000/demo/pyindex:latest /mnt
