"""Installer logic. Used by pip."""
from setuptools import setup

setup(
    name = "storas",
    version = "0.1",
    description = "A replacement for Android's repo tool",
    url = None,
    author = "Eli Ribble",
    extras_require = {
        "develop" : [
            "mypy==0.670",
            "nose2",
            "pre-commit==1.14.4",
            "pylint==2.3.1",
        ]
    },
    install_requires = [
		"tabulate==0.8.3",
    ],
    scripts = [
        'bin/storas',
    ],
    packages = ['storas'],
    package_data = {
       'storas' : ['storas/*'],
    },
)
