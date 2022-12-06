#!/bin/bash

set -x
SRC_DIR=protos
DST_DIR=emporous_pip/generated
#PYI_DIR=types

#protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/manager.proto
#python -m grpc_tools.protoc -I"generated=$SRC_DIR" --python_out="$DST_DIR" --pyi_out="$DST_DIR" --grpc_python_out="$DST_DIR" "$SRC_DIR/manager.proto"
python -m grpc_tools.protoc -I"$SRC_DIR" --python_out="$DST_DIR" --pyi_out="$DST_DIR" --grpc_python_out="$DST_DIR" "$SRC_DIR/manager.proto"
#python -m grpc_tools.protoc -I"$SRC_DIR" --pyi_out="$PYI_DIR" "$SRC_DIR/manager.proto"

#python -m grpc_tools.protoc -Iprotos --python_out=./emporous_pip --pyi_out=./emporous_pip --grpc_python_out=./emporous_pip ./protos/manager.proto
#python -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/emporous_pip/generated/manager.proto

