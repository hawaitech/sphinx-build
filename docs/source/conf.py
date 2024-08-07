# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
os.environ['SPHINX_APIDOC_OPTIONS']='members,show-inheritance'

import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', '../src')))

project = '>Sphinx-builder'
copyright = '2024, HawAI.tech'
author = 'HawAI.tech'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'sphinxcontrib.apidoc',
   'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

apidoc_module_dir = '../../src/'
apidoc_output_dir = 'source'
apidoc_separate_modules = True