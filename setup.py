import setuptools
from supernodes import __version__

with open("README.md", "r") as file:
    long_description = file.read()

name = "SuperNodes"
version = __version__
author = "Mubarak Almehairbi"
description = "Creates tree data structures easily"
package_name = "supernodes"
with open(f"{package_name}/requirements.txt", "rt") as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name=package_name,                     # This is the name of the package
    version=version,                        # The initial release version
    author=author,                     # Full name of the author
    description=description,
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=[package_name],             # Name of the python package
    install_requires=requirements                     # Install other dependencies if any
)