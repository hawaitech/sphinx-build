#!/bin/sh

SOURCE_ROOT=$1
BUILD_ROOT=$2
BRANCH_NAME=$3

DST_DIR=$BUILD_ROOT/$GITHUB_REPOSITORY/$BRANCH_NAME
mkdir -p $DST_DIR

export TZ=UTC  # TZ is because of bazel issue see https://github.com/nektos/act/issues/1853
export PYTHONPATH="/ext:$SOURCE_ROOT/ext"

if [ -f "$SOURCE_ROOT/requirements.txt" ]; then
    UV_WITH=--with-requirements=$SOURCE_ROOT/requirements.txt
else
    UV_WITH=--with sphinx
fi

UV_CMD=uv run $UV_WITH --no-project sphinx-build $GITHUB_WORKSPACE/$SOURCE_ROOT $BUILD_ROOT/$GITHUB_REPOSITORY/$BRANCH_NAME

echo $UV_CMD
$UV_CMD
