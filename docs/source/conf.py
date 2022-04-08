import os
import sys

import bpy
import addon_utils

from sphinx.builders.html import StandaloneHTMLBuilder
StandaloneHTMLBuilder.supported_image_types = [
    'image/svg+xml',
    'image/gif',
    'image/png',
    'image/jpeg'
]

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('..'))))

import bhq_addon_base as addon

project = 'BlenderHQ Addon Base'
copyright = '2022, Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)'
author = 'Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)'

version = '.'.join((str(_) for _ in addon_utils.module_bl_info(addon)["version"]))
release = 'rc'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
language = 'en'
exclude_patterns = []

autodoc_member_order = 'bysource'

html_theme = 'sphinx_rtd_theme'
html_logo = "bhq_logo_color_v0.svg"
html_static_path = []
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 2,
    'includehidden': True,
    'titles_only': False
}
