SOURCE_ROOT=$1
BUILD_ROOT=$1

echo "$SOURCE_ROOT \n $BUILD_ROOT"

if [ -f "$SOURCE_ROOT/requirements.txt"]; then
    pip install -r $SOURCE_ROOT/requirements.txt

sphinx-build -M html $SOURCE_ROOT $BUILD_ROOT