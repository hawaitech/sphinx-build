#!/bin/sh

SOURCE_ROOT=$1
BUILD_ROOT=$2
BRANCH_NAME=$3

DST_DIR=$BUILD_ROOT/$GITHUB_REPOSITORY/$BRANCH_NAME
mkdir -p $DST_DIR

export TZ=UTC  # TZ is because of bazel issue see https://github.com/nektos/act/issues/1853
export PYTHONPATH="/ext:$SOURCE_ROOT/ext"

echo "installing pandoc"
apt-get update && apt-get install -y pandoc

echo "Setup uv"
uv venv -p 3.12 .venv
uv pip install -U sphinx

if [ -f "$SOURCE_ROOT/requirements.txt" ]; then
    echo "Installation of requirements"
    uv pip install -r $SOURCE_ROOT/requirements.txt
else
    echo "No installation requirements found"
fi

uv run sphinx-build $GITHUB_WORKSPACE/$SOURCE_ROOT $BUILD_ROOT/$GITHUB_REPOSITORY/$BRANCH_NAME
