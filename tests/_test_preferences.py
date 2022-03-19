import os
import string

import bpy

from .. import registration
from .. import ui

_SAMPLE_TEXT = None


def sample_text():
    global _SAMPLE_TEXT

    if _SAMPLE_TEXT is None:
        with open(os.path.join(os.path.dirname(__file__), "SAMPLE_TEXT.txt")) as file:
            _SAMPLE_TEXT = file.read()

    if _SAMPLE_TEXT is None:
        return "Unable to read sample text file"
    return _SAMPLE_TEXT


def test_draw_wrapped_text(context, layout):
    compact_ui = context.region.width < 450

    addon_pref = registration.addon_preferences(context)

    if compact_ui:
        layout.prop(addon_pref, "wrapped_text_tab")
    else:
        row = layout.row(align=True)
        row.prop(addon_pref, "wrapped_text_tab", expand=True)

    if addon_pref.wrapped_text_tab == 'CHAR':
        if compact_ui:
            layout.prop(addon_pref, "wrapped_text_char")
        else:
            grid = layout.grid_flow(row_major=True, columns=20, even_columns=True, align=True)
            grid.use_property_split = False
            grid.prop(addon_pref, "wrapped_text_char", expand=True)
        layout.prop(addon_pref, "wrapped_text_char_interval")
    layout.prop(addon_pref, "wrapped_text_length")
    layout.label(
        text=f"`.utils_ui.draw_wrapped_text` "
        f"(region width: {context.region.width}px, type: \'{context.region.type}\')",
        icon='INFO'
    )

    if addon_pref.wrapped_text_tab == 'LONG':
        text = sample_text()
        if addon_pref.wrapped_text_length > 0:
            if addon_pref.wrapped_text_length < len(text):
                text = text[0:addon_pref.wrapped_text_length]
            elif addon_pref.wrapped_text_length > len(text):
                num_iterations = int(addon_pref.wrapped_text_length / len(text))
                if num_iterations > 1:
                    text *= num_iterations
                num_chars_left = addon_pref.wrapped_text_length - len(text)
                text += text[0:num_chars_left]

    elif addon_pref.wrapped_text_tab == 'CHAR':
        num_chars = 500
        if addon_pref.wrapped_text_length > 0:
            num_chars = addon_pref.wrapped_text_length

        text = ""
        num_iterations = int(num_chars / addon_pref.wrapped_text_char_interval)

        if num_iterations < 1:
            text = addon_pref.wrapped_text_char * num_chars
        else:
            text = ((addon_pref.wrapped_text_char * addon_pref.wrapped_text_char_interval) + ' ') * num_iterations

    layout.label(text=f"Text Block ({len(text)} characters):", icon='INFO')
    ui.draw_wrapped_text(context, layout, text=text)


class BHQABT_Preferences(bpy.types.AddonPreferences):
    bl_idname = registration.current_addon().__package__

    tab: bpy.props.EnumProperty(
        items=(
            ('WRAPPED_TEXT', "Wrapped Text", ""),
            ('INFO', "Info", ""),
        )
    )

    wrapped_text_tab: bpy.props.EnumProperty(
        items=(
            ('LONG', "Long Text Block", ""),
            ('CHAR', "Single Character", ""),
        ),
        default='LONG',
        name="Text Block",
    )

    wrapped_text_char: bpy.props.EnumProperty(
        items=[(_, _, _) for _ in string.printable],
        default='A',
        name="Character",
    )

    wrapped_text_char_interval: bpy.props.IntProperty(name="Spacer Interval", default=10, min=1)
    wrapped_text_length: bpy.props.IntProperty(name="Text Length", default=-1, min=-1)

    @ui.template_addon_versioning(url_help=registration.addon_doc_url())
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop_tabs_enum(self, "tab")
        if self.tab == 'WRAPPED_TEXT':
            test_draw_wrapped_text(context, layout)
        elif self.tab == 'INFO':
            ui.template_qr_code_links(
                layout=layout,
                links=(
                    ("qr.bhqab_github", "https://github.com/BlenderHQ/bhq_addon_base", "GitHub Repository"),
                    ("qr.bhq_github", "https://github.com/BlenderHQ", "BlenderHQ on GitHub"),
                    ("qr.bhq_patreon", "https://www.patreon.com/BlenderHQ", "BlenderHQ on Patreon"),
                )
            )
