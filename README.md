# Banger - Project Version Bumper

This is github action for bumping project version. You have to provide a list
of files where project version is defined - and then, this github action will
look into that list of files and increment version which it finds.

As of now, banger will increment only micro part of the version - i.e. the patch version.
Version format in version file must have one of the following formats:

    version = "<version in PEP 440>"
    version = '<version in PEP 440>'
    __version__ = "<version in PEP 440>"
    __version__ = '<version in PEP 440>'

There is only one space character surrounding equal sign ('=').
For version examples see [packaging documentation](https://packaging.pypa.io/en/latest/version.html).
Detailed [PEP 440](https://peps.python.org/pep-0440/).

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

Run tests:

    pytest

Run from command line main module in dry run mode:

     PYTHONPATH=. INPUT_FILES_LIST=pyproject.toml,example-data/version.py python ./banger/main.py

Above command will look for version in files ``pyproject.toml, example-data/version.py`` and
increment the patch part of the version and replace new version in ``pyptoject.toml, example-data/version.py``
files.


## References

* [Creating GitHub Actions in Python](https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/)
