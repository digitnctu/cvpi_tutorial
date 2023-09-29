# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cvpi_tutorial'
copyright = '2023, digit_nctu@yahoo.com.tw'
author = 'digit_nctu@yahoo.com.tw'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinxcontrib.plantuml','sphinx.ext.graphviz','sphinxcontrib.wavedrom']
#plantuml = 'java -jar plantuml-1.2023.1.jar'
render_using_wavedrompy = True

templates_path = ['_templates']
exclude_patterns = []
# online_wavedrom_js_url = 'albert'

language = 'big5'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
