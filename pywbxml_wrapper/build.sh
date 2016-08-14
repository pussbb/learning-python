#!/bin/bash

CURR_DIR="$( realpath $( dirname "${BASH_SOURCE[0]}") )/"

LIBWBXML_DIR="$CURR_DIR/libwbxml/"

if [ ! -d "$LIBWBXML_DIR" ]; then
    echo "Please download libwbxml and unpack into folder '$LIBWBXML_DIR' "
fi
if [ ! -d "$LIBWBXML_DIR/build" ]; then
    mkdir -p "$LIBWBXML_DIR/build"
fi

cd "$LIBWBXML_DIR/build/"
cmake wbxml2_static -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS=-fPIC -DBUILD_STATIC_LIBS=ON -DENABLE_INSTALL_DOC=OFF -DCMAKE_INSTALL_PREFIX="$CURR_DIR/wbxmldist" -DLIB_SUFFIX="" $LIBWBXML_DIR
make wbxml2_static
make wbxml2_static install

cd "$CURR_DIR"
python3 setup.py build_ext --inplace
strip pywbxml.cpython*
python3 test.py