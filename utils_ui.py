# <pep8 compliant>

import random
import string

import bpy
import blf
from bl_ui import space_statusbar

from . import utils_extend_bpy_types


def _string_width(string: str) -> float:
    if len(string) == 1:
        num_single_ch_samples = 100
        return blf.dimensions(0, string * num_single_ch_samples)[0] / num_single_ch_samples
    return blf.dimensions(0, string)[0]


def draw_wrapped_text(context: bpy.types.Context, layout: bpy.types.UILayout, text: str) -> None:
    """Draws a block of text in the given layout, dividing it into lines
    according to the width of the current region of the interface.

    .. Warning::
        The function uses a fairly accurate but at the same time relatively slow
        way to format strings. Not recommended for use with very large blocks
        of text as this may slow down the overall user interface.

    Args:
        context (`bpy.types.Context`_): Current context.
        layout (`bpy.types.UILayout`_): Current layout.
        text (str): Text to be wrapped and drawn.
    """

    col = layout.column(align=True)

    if context.region.type == 'WINDOW':
        win_padding = 25
    elif context.region.type == 'UI':
        win_padding = 52
    else:
        win_padding = 52

    wrap_width = context.region.width - win_padding
    space_width = _string_width(' ')

    for line in text.split('\n'):
        num_characters = len(line)

        if not num_characters:
            continue

        line_words = list((_, _string_width(_)) for _ in line.split(' '))
        num_line_words = len(line_words)
        line_words_last = num_line_words - 1

        sublines = [""]
        subline_width = 0.0

        for i in range(num_line_words):
            word, word_width = line_words[i]

            sublines[-1] += word
            subline_width += word_width

            next_word_width = 0.0
            if i < line_words_last:
                next_word_width = line_words[i + 1][1]

                sublines[-1] += ' '
                subline_width += space_width

            if subline_width + next_word_width > wrap_width:
                subline_width = 0.0
                if i < line_words_last:
                    sublines.append("")  # Add new subline.

        for subline in sublines:
            col.label(text=subline)


def developer_extras_poll(context: bpy.types.Context) -> bool:
    """A method for determining whether a user interface intended for developers should be displayed.

    Args:
        context (`bpy.types.Context`_): Current context.

    Returns:
        bool: A positive value means that it should.
    """
    return context.preferences.view.show_developer_ui


def template_developer_extras_warning(context: bpy.types.Context, layout: bpy.types.UILayout) -> None:
    """Output message in the user interface that this section of the interface
    is visible because the active options in the Blender settings. These
    options are also displayed with the ability to disable them.

    Args:
        context (`bpy.types.Context`_): Current context.
        layout (`bpy.types.UILayout`_): Current UI layout.
    """
    if developer_extras_poll(context):
        col = layout.column(align=True)
        col.label(text="Warning", icon='INFO')
        text = "This section is intended for developers. You see it because " \
            "you have an active \"Developers Extras\" option in the Blender " \
            "user preferences."
        draw_wrapped_text(context, col, text)
        col.prop(context.preferences.view, "show_developer_ui")


def _update_statusbar():
    # TODO: Current implementation works but should be replaced with more
    # appropriate. Currently there is no any alternatives.
    bpy.context.workspace.status_text_set(None)


class _progress_meta(type):
    @property
    def PROGRESS_BAR_UI_UNITS(cls):
        return cls._PROGRESS_BAR_UI_UNITS

    @PROGRESS_BAR_UI_UNITS.setter
    def PROGRESS_BAR_UI_UNITS(cls, value):
        cls._PROGRESS_BAR_UI_UNITS = max(cls._PROGRESS_BAR_UI_UNITS_MIN, min(value, cls._PROGRESS_BAR_UI_UNITS_MAX))


class progress(metaclass=_progress_meta):
    """A class that implements the initialization and completion of progressbars.
    The module provides the ability to display the progressbar (and even several
    progressbars) in the status bar of the Blender. This technique can be used
    mainly with modal operators that run for a relatively long time and require
    the output of the progress of their work.

    Attributes:
        PROGRESS_BAR_UI_UNITS (int): Number of UI units in range [4...12] used
            for progressbar without text label and icon.
    """

    _PROGRESS_BAR_UI_UNITS = 6
    _PROGRESS_BAR_UI_UNITS_MIN = 4
    _PROGRESS_BAR_UI_UNITS_MAX = 12

    _is_drawn = False
    _attrname = ""

    class ProgressPropertyItem(bpy.types.PropertyGroup):
        """Progress bar item that allows you to dynamically change some display parameters.

        Attributes:
            num_steps (int): Number of progress steps.
            step (int): Current progress step.
            value (float): Evaluated progress value (readonly).
            icon (str): Blender icon to be displayed.
            icon_value (int): Icon id to be displayed.
            label (str): Progressbar text label.
            cancellable (bool): Positive value means that progressbar should draw cancel button.
        """

        def _common_value_update(self, _context):
            _update_statusbar()

        valid: bpy.props.BoolProperty(
            default=True,
            update=_common_value_update,
        )

        num_steps: bpy.props.IntProperty(
            min=1,
            default=1,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )

        step: bpy.props.IntProperty(
            min=0,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )

        def _get_progress(self):
            return (self.step / self.num_steps) * 100

        def _set_progress(self, _value):
            pass

        value: bpy.props.FloatProperty(
            min=0.0,
            max=100.0,
            precision=1,
            get=_get_progress,
            # set=_set_progress,
            subtype='PERCENTAGE',
            options={'HIDDEN'},
        )

        icon: bpy.props.StringProperty(
            default='NONE',
            maxlen=64,
            options={'HIDDEN'},
            update=_common_value_update,
        )

        icon_value: bpy.props.IntProperty(
            min=0,
            default=0,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )

        label: bpy.props.StringProperty(
            default="Progress",
            options={'HIDDEN'},
            update=_common_value_update,
        )

        cancellable: bpy.props.BoolProperty(
            default=False,
            options={'HIDDEN'},
            update=_common_value_update,
        )

    def _func_draw_progress(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.template_input_status()
        layout.separator_spacer()
        layout.template_reports_banner()

        if hasattr(bpy.types.WindowManager, progress._attrname):
            layout.separator_spacer()
            for item in progress.valid_progress_items():
                row = layout.row(align=True)
                row.label(text=item.label, icon=item.icon, icon_value=item.icon_value)

                srow = row.row(align=True)
                srow.ui_units_x = progress.PROGRESS_BAR_UI_UNITS
                srow.prop(item, "value", text="")

                if item.cancellable:
                    row.prop(item, "valid", text="", icon='X', toggle=True, invert_checkbox=True)

        layout.separator_spacer()

        row = layout.row()
        row.alignment = 'RIGHT'

        row.label(text=context.screen.statusbar_info(), translate=False)

    @classmethod
    def progress_items(cls):
        return getattr(bpy.context.window_manager, cls._attrname)

    @classmethod
    def valid_progress_items(cls):
        return (_ for _ in cls.progress_items() if _.valid)

    @classmethod
    def invoke(cls) -> ProgressPropertyItem:
        """Invoke new progressbar for each call.

        Returns:
            ProgressPropertyItem: New initialized progress property item.
        """

        if not cls._is_drawn:
            bpy.utils.register_class(progress.ProgressPropertyItem)
            cls._attrname = utils_extend_bpy_types.unique_name(
                collection=bpy.types.WindowManager,
                prefix="bhq_",
                suffix="_progress"
            )

            setattr(
                bpy.types.WindowManager,
                cls._attrname,
                bpy.props.CollectionProperty(type=progress.ProgressPropertyItem)
            )

            bpy.types.STATUSBAR_HT_header.draw = cls._func_draw_progress
            _update_statusbar()

        cls._is_drawn = True
        return cls.progress_items().add()

    @classmethod
    def complete(cls, item: ProgressPropertyItem):
        """Removes progressbar from UI. If removed progressbar was the last one,
        would be called
        :py:func:`progress.release_all` class method.

        Args:
            item (ProgressPropertyItem): Progress item to be removed.
        """
        assert(isinstance(item, progress.ProgressPropertyItem))

        item.valid = False

        for _ in cls.valid_progress_items():
            return
        cls.release_all()

    @classmethod
    def release_all(cls):
        """Removes all progressbars."""
        if not cls._is_drawn:
            return

        from importlib import reload

        assert(cls._attrname)
        delattr(bpy.types.WindowManager, cls._attrname)
        bpy.utils.unregister_class(progress.ProgressPropertyItem)

        reload(space_statusbar)
        bpy.types.STATUSBAR_HT_header.draw = space_statusbar.STATUSBAR_HT_header.draw
        _update_statusbar()

        del reload

        cls._is_drawn = False
