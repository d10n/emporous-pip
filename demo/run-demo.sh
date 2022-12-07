#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit

run_cmd="$(command -pv podman || command -pv docker)"
# This demo uses containerd and runc, so the --privileged flag is used.
"${run_cmd}" run -it --rm --privileged -v mytmp:/tmp -v myvar:/var -v "$PWD"/output:/output "$1"
"${run_cmd}" volume rm mytmp
"${run_cmd}" volume rm myvar
