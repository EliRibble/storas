# storas

Storas is a replacement for the AOSP (Android Open Source Project)'s 'repo'
tool. It aims to do the following:

1. Not break all the time in obscure ways.
1. Leverage git submodules as much as possible for tighter git integration.
1. Be native Python 3.

## Etymology

This is what I got for the Gaelic translation of "repository". 

## Hacking

Clone the repository. Then run `pip install -e .[develop]` in the cloned
repository. This should install all the developer dependencies. Then you run
`pre-commit install` to setup the pre-commit hooks.
