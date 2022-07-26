# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'threatware'
copyright = '2022, samadhicsecurity.com'
author = 'dave@samadhicsecurity.com'

release = '0.9'
version = '0.9.2'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

#master_doc = 'index.md'

templates_path = ['_templates']

source_suffix = ['.md']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Options for MyST

myst_heading_anchors = 3
myst_enable_extensions = ["deflist", "colon_fence"]