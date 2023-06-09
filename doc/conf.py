# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
sys.path.insert(0,os.path.abspath('..'))
from supernodes import __version__

project = 'SuperNodes'
copyright = '2023, Mubarak Almehairbi'
author = 'Mubarak Almehairbi'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.viewcode','sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.todo',
              'sphinx.ext.autosummary', 'myst_parser', 'sphinx.ext.intersphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_theme_options = {
   "show_nav_level": 0
}
html_static_path = ['_static']
