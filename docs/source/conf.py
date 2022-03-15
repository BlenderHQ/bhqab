import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('..'))))

import qrcode
import qrcode.image.svg

image_factory = qrcode.image.svg.SvgPathFillImage

qr_bhqab_github_io = qrcode.make("https://blenderhq.github.io/bhq_addon_base/", image_factory=image_factory)
qr_bhqab_github_io.save(os.path.abspath("./images/qr_bhqab_github_io.svg"))

qr_bhqab_github = qrcode.make("https://github.com/BlenderHQ/bhq_addon_base", image_factory=image_factory)
qr_bhqab_github.save(os.path.abspath("./images/qr_bhqab_github.svg"))

qr_bhq_github = qrcode.make("https://github.com/BlenderHQ", image_factory=image_factory)
qr_bhq_github.save(os.path.abspath("./images/qr_bhq_github.svg"))

qr_bhq_patreon = qrcode.make("https://www.patreon.com/BlenderHQ", image_factory=image_factory)
qr_bhq_patreon.save(os.path.abspath("./images/qr_bhq_patreon.svg"))

from sphinx.builders.html import StandaloneHTMLBuilder
StandaloneHTMLBuilder.supported_image_types = [
    'image/svg+xml',
    'image/gif',
    'image/png',
    'image/jpeg'
]

project = 'BlenderHQ Addon Base'
copyright = '2022, Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)'
author = 'Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)'

release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
]

numfig = True
autodoc_member_order = 'bysource'
templates_path = ['_templates']
exclude_patterns = []
html_static_path = []
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': False,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_logo = "bhq_logo_color_v0.svg"