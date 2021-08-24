# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import pathlib

from pallets_sphinx_themes import ProjectLink


sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "Flask-Shell2HTTP"
copyright = "2020, Eshaan Bansal"
author = "Eshaan Bansal"

# The full version, including alpha/beta/rc tags
release = (pathlib.Path(__file__).parent.parent.parent / "version.txt").read_text()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "recommonmark",
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "flask"

# Custom options

html_context = {
    "project_links": [
        ProjectLink("Donate To The Author", "https://paypal.me/eshaanbansal"),
        ProjectLink(
            "Flask-Shell2HTTP Website", "https://flask-shell2http.readthedocs.io/"
        ),
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask-Shell2HTTP/"),
        ProjectLink("Source Code", "https://github.com/eshaan7/flask-shell2http"),
        ProjectLink(
            "Issue Tracker", "https://github.com/eshaan7/flask-shell2http/issues"
        ),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
# html_favicon = "_static/flask-icon.png"
# html_logo = "_static/flask-icon.png"
html_title = f"Flask-Shell2HTTP Documentation ({release})"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
