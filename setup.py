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
	scripts=[
	],
	packages=['storas'],
	package_data={
	   'storas' : ['storas/*'],
	},
)
