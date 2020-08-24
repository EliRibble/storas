# storas

Storas was originally designed as a replacement for the AOSP
(Android Open Source Project)'s 'repo' tool. It aims to do the following.

Turns out I don't like 'repo' and don't want to re-implement it anyways
because I don't think it, as a tool, is a good idea.

So instead this repository just became a toolkit for dealing with 'repo'
manifest files. I use them to help create tools for migrating off of 'repo'.

## Etymology

This is what I got for the Gaelic translation of "repository". 

## Hacking

You'll want to install the developer dependencies:

```
pip install -e .[develop]
```

This will include `nose2`, which is the test runner of choice. After you make modifications you can run tests with

```
nose2
```

When you're satisfied you'll want to update the version number and do build-and-upload:

```
python setup.py sdist bdist_wheel
twine upload dist/* --verbose
```
