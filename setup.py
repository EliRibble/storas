"""Installer logic. Used by pip."""
from setuptools import setup # type: ignore

setup(
    name="storas",
    version="0.1",
    description="A replacement for Android's repo tool",
    url=None,
    author="Eli Ribble",
    extras_require={
        "develop" : [
            "mypy==0.770",
            "nose2",
            "pre-commit==1.14.4",
            "pylint==2.3.1",
            "wheel",
        ]
    },
    install_requires=[
    ],
    scripts=[
    ],
    packages=['storas'],
    package_data={
       'storas' : ['storas/*'],
    },
)
