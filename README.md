# Sphnx builder action

This action install a requirements.txt in `src-root` if their is one. After it will use sphinx-build to build static html files in directory `build-root` of documentation about the code in `src-root`.

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

## New directives

The directory **ext** offers some new rst directives. For now, their is directives for ros documentation. To see documentation about it see the README in this directory.

Those directives are used by the action, they can be used within your documentation by adding the file name in the *extensions* parameter within **conf.py**. For example, to use directives implemented in **ros_directives.py** add "ros_directives" within your *exetensions* parameter.
