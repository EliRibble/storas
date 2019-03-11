from setuptools import setup

setup(
    name = "storas",
    version = "0.1",
    description = "A replacement for Android's repo tool",
    url = None,
    author = "Eli Ribble",
    extras_require = {
        "develop" : [
            "nose2"
        ]
    },
    install_requires = [
    ],
    scripts = [
        'bin/storas',
    ],
    packages = ['storas'],
    package_data = {
        'storas' : ['storas/*'],
    },
)
