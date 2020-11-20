"""Installer logic. Used by pip."""
from setuptools import setup # type: ignore

setup(
	extras_require={
		"develop" : [
			"mypy",
			"nose2",
			"pre-commit",
			"pylint",
			"twine",
			"wheel",
		]
	},
	install_requires=[
	],
)
