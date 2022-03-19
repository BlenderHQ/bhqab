import os
import sys

import bpy
import addon_utils

import qrcode
import qrcode.image.svg

from sphinx.builders.html import StandaloneHTMLBuilder
StandaloneHTMLBuilder.supported_image_types = [
    'image/svg+xml',
    'image/gif',
    'image/png',
    'image/jpeg'
]

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('..'))))

import bhq_addon_base as addon


def _generate_qr_code(url: str, name: str):
    image_factory = qrcode.image.svg.SvgPathFillImage

    image_svg = qrcode.make(url, image_factory=image_factory)
    image_svg.save(os.path.abspath(f"./images/{name}.svg"))

    image = qrcode.make(url, border=2)
    image.save(os.path.abspath(f"./images/{name}.png"))


_generate_qr_code("https://blenderhq.github.io/bhq_addon_base/", "qr_bhqab_github_io")
_generate_qr_code("https://github.com/BlenderHQ/bhq_addon_base", "qr_bhqab_github")
_generate_qr_code("https://github.com/BlenderHQ", "qr_bhq_github")
_generate_qr_code("https://www.patreon.com/BlenderHQ", "qr_bhq_patreon")

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
html_theme = 'sphinx_rtd_theme'
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
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_logo = "bhq_logo_color_v0.svg"
scv_banner_greatest_tag = True
scv_grm_exclude = ('.gitignore', '.nojekyll', 'README.rst')
scv_show_banner = True
scv_sort = ('semver', 'time')
