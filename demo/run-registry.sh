#!/bin/bash

registry serve /projects/config-dev.yml >/output/registry.log 2>&1 &
containerd >/output/containerd.log 2>&1 &
wait
