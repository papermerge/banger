# Banger - Project Version Bumper

This is GitHub action for bumping project version.

You provide a list of files where project version is defined and banger GitHub action will
iterate given list of files and perform following steps with each of them:
1. detected project version (so called `old version`) e.g. 2.1.29
2. increment it e.g. 2.1.30
3. and finally it will overwrite respective file with incremented version (`new version`)

As of now, banger will increment only micro part of the version - i.e. the patch version.

Following files types are supported:

* python
* javascript
* json

For **python files**, version format in version file must have one of the following formats:
```
version = "<version in PEP 440>"
version = '<version in PEP 440>'
__version__ = "<version in PEP 440>"
__version__ = '<version in PEP 440>'
```
There is only one space character surrounding equal sign (`=`).
Version string must end with newline character (`\n`).
For version examples see [packaging documentation](https://packaging.pypa.io/en/latest/version.html).
Detailed [PEP 440](https://peps.python.org/pep-0440/).

For **javascript file**, version file is expected to have the following structure:
```
export const version = "<version in PEP 440>";
```
single quote strings are accepted as well:
```
export const version = '<version in PEP 440>';
```
Notice that `;` character is mandatory, and it must be followed by new line (`\n`).


For **json files** works only with npm specific package.json file. Following structure is expected:
```
{
  ...
  "name": "papermerge",
  "version": "<version in PEP 440>",
  "description": ...
 }
```

Notice that version string must end with comma (`,`) and new line (`\n`).

## Usage

### Example workflow

```yaml
name: Version bump

on: [workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master

      - name: Version bump
        id: version-bump

        uses: papermerge/banger@master
        with:
          files_list: "pyproject.toml,example-data/version.py"

      - name: Commit files
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git commit -m "version bump ${{steps.version-bump.outputs.OLD_VERSION}} -> ${{steps.version-bump.outputs.NEW_VERSION}}" -a

      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `files_list`  | Comma delimited list of files where to look for the versions to increment    |


### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `old_version`  | Project's version before the increment    |
| `new_version`  | Project's version after the increment    |


Note that only the last file in the input list is used to set the output - this means that you
need to make sure that each mentioned file has same version - after all a given project can
have only a single version (in given git branch).

### Test

Run tests using pytest:
```
pytest
```

Run from command line main module in dry run mode:

```
PYTHONPATH=. INPUT_FILES_LIST=pyproject.toml,example-data/version.py python ./banger/main.py
```

Above command will look for version in files ``pyproject.toml, example-data/version.py`` and
increment the patch part of the version and replace new version in ``pyptoject.toml, example-data/version.py``
files.

Or if you want to check version bumping on javascript file:

```
PYTHONPATH=. INPUT_FILES_LIST=example-data/version.js python ./banger/main.py
```

It is also possible to bump version found in json file

```
PYTHONPATH=. INPUT_FILES_LIST=example-data/package.json python ./banger/main.py
```

## References

* [Creating GitHub Actions in Python](https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/)
