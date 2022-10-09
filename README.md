# Python Container Action Template

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/jacobtomlinson/python-container-action)
[![Actions Status](https://github.com/jacobtomlinson/python-container-action/workflows/Lint/badge.svg)](https://github.com/jacobtomlinson/python-container-action/actions)
[![Actions Status](https://github.com/jacobtomlinson/python-container-action/workflows/Integration%20Test/badge.svg)](https://github.com/jacobtomlinson/python-container-action/actions)


## Usage

Describe how to use your action here.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action

      # Put your action repo here
      uses: me/myaction@master

      # Put an example of your mandatory inputs here
      with:
        myInput: world
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples

> NOTE: People ❤️ cut and paste examples. Be generous with them!

### Using the optional input

This is how to use the optional input.

```yaml
with:
  myInput: world
  anotherInput: optional
```

### Using outputs

Show people how to use your outputs in another action.

```yaml
steps:
- uses: actions/checkout@master
- name: Run action
  id: myaction

  # Put your action name here
  uses: me/myaction@master

  # Put an example of your mandatory arguments here
  with:
    myInput: world

# Put an example of using your outputs here
- name: Check outputs
    run: |
    echo "Outputs - ${{ steps.myaction.outputs.myOutput }}"
```


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
