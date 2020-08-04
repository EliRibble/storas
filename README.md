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

Clone the repository. Then run `pip install -e .[develop]` in the cloned
repository. This should install all the developer dependencies. Then you run
`pre-commit install` to setup the pre-commit hooks.
