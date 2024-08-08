# Sphnx builder action

This action install a requirements.txt in `src-root` if their is one. After it will use sphinx-build to build static html files in directory `build-root` of documentation about the code in `src-root`

## Inputs

### `src-root`

**Not Required** The path where is the python package. Default `"/docs/source"`.

### `build-root`

**Not Required** The path where is build html files. Default `"/docs/build"`.

## Example usage
```
uses: JulesFa/sphinx-build@main
with:
  src-root: "path-to-src"
  build-root: "path-to-build"
```
