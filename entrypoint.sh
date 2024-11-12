#!/bin/bash

SOURCE_ROOT=$1
BUILD_ROOT=$2
BRANCH_NAME=$3

echo "branch_name =" 
echo ${BRANCH_NAME}
mkdir -p $BUILD_ROOT/$GITHUB_REPOSITORY/$BRANCH_NAME

python3 -m venv .venv

echo $(.venv/bin/python --version)
if [ -f "$SOURCE_ROOT/requirements.txt" ]; then
    echo "Installation of requirements"
    .venv/bin/pip install -U sphinx
    .venv/bin/pip install -r $SOURCE_ROOT/requirements.txt
else
    echo "No installation requirements found"
fi

# TZ is because of bazel issue see https://github.com/nektos/act/issues/1853
TZ=UTC .venv/bin/sphinx-build $GITHUB_WORKSPACE/$SOURCE_ROOT $BUILD_ROOT/$GITHUB_REPOSITORY/${BRANCH_NAME:11:$length}
