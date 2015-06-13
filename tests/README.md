# similarweb unit tests

If you're reading this, you (hopefully) want to contribute! Here's how to get the test suite up-and-running.

## Setup
From the root directory of this repo:

```
$ python setup.py develop
$ pip install -r tests/requirements.txt
```

## Running the test suite
From the root directory of this repo:

```
$ py.test
```

You can see more detailed output by adding the `-vv` flag:

```
$ py.test -vv
```

