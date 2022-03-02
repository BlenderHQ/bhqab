# <pep8 compliant>

import random
import string

import bpy
import blf
from bl_ui import space_statusbar


WIN_PADDING = 32


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
        context (bpy.types.Context): Current context.
        layout (bpy.types.UILayout): Current layout.
        text (str): Text to be wrapped and drawn.
    """

    col = layout.column(align=True)

    wrap_width = context.region.width - WIN_PADDING
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


def _update_statusbar():
    # TODO: Current implementation works but should be replaced with more
    # appropriate. Currently there is no any alternatives.
    bpy.context.workspace.status_text_set(None)


class progress:
    """A class that implements the initialization and completion of progressbars.
    The module provides the ability to display the progressbar (and even several
    progressbars) in the status bar of the Blender. This technique can be used
    mainly with modal operators that run for a relatively long time and require
    the output of the progress of their work.
    """

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

        def _get_index(self) -> int:
            if "index" in self:
                return self["index"]
            return 0

        def _set_index(self, value: int) -> None:
            if value == 0:
                self["index"] = 0
            elif not self.index:
                self["index"] = value

        def _common_value_update(self, _context):
            _update_statusbar()

        index: bpy.props.IntProperty(
            options={'HIDDEN'},
            get=_get_index,
            set=_set_index,
        )

        num_steps: bpy.props.IntProperty(
            min=1,
            default=1,
            options={'HIDDEN'},
            update=_common_value_update,
        )

        step: bpy.props.IntProperty(
            min=0,
            options={'HIDDEN'},
            update=_common_value_update,
        )

        def _get_progress(self):
            return self.step / self.num_steps

        def _set_progress(self, value):
            pass

        value: bpy.props.FloatProperty(
            min=0.0,
            max=1.0,
            get=_get_progress,
            set=_set_progress,
            subtype='PERCENTAGE',
            options={'HIDDEN'},
        )

        icon: bpy.props.StringProperty(
            default='NONE',
            options={'HIDDEN'},
            update=_common_value_update,
        )

        icon_value: bpy.props.IntProperty(
            options={'HIDDEN'},
            update=_common_value_update,
        )

        label: bpy.props.StringProperty(
            default="Progress",
            options={'HIDDEN'},
            update=_common_value_update,
        )

        cancellable: bpy.props.BoolProperty(
            options={'HIDDEN'},
            update=_common_value_update,
        )

        cancel: bpy.props.BoolProperty(
            name="Cancel",
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
            progress_items = getattr(context.window_manager, progress._attrname)

            layout.separator_spacer()
            for item in progress_items:
                row = layout.row(align=True)
                row.prop(item, "value", text=item.label, icon=item.icon, icon_value=item.icon_value)
                if item.cancellable:
                    row.prop(item, "cancel", text="", icon='X', toggle=True)

        layout.separator_spacer()

        row = layout.row()
        row.alignment = 'RIGHT'

        row.label(text=context.screen.statusbar_info(), translate=False)

    _is_drawn = False
    _attrname = ""

    @staticmethod
    def _generate_wm_attr_name() -> str:
        """Generates random attribute name for `bpy.types.WindowManager`.

        Returns:
            str: Attribute name.
        """
        def _random_str() -> str:
            return "".join((random.choice(string.ascii_lowercase) for _ in range(5)))

        attr = _random_str()
        while hasattr(bpy.types.WindowManager, attr):
            attr = _random_str()

        return attr

    @classmethod
    def invoke(cls) -> ProgressPropertyItem:
        """Invoke new progressbar for each call.

        Returns:
            ProgressPropertyItem: New initialized progress property item.
        """
        def _add_item():
            progress_items = getattr(bpy.context.window_manager, cls._attrname)
            item = progress_items.add()
            item.index = len(progress_items) - 1
            return item

        if cls._is_drawn:
            return _add_item()
        else:
            bpy.utils.register_class(progress.ProgressPropertyItem)
            cls._attrname = cls._generate_wm_attr_name()

            setattr(
                bpy.types.WindowManager,
                cls._attrname,
                bpy.props.CollectionProperty(type=progress.ProgressPropertyItem)
            )

            bpy.types.STATUSBAR_HT_header.draw = cls._func_draw_progress
            _update_statusbar()

            cls._is_drawn = True

            return _add_item()

    @classmethod
    def complete(cls, item: ProgressPropertyItem):
        """Removes progressbar from UI. If removed progressbar was the last one,
        would be called
        :func:..py:currentmodule::`progress.release_all` class method.

        Args:
            item (ProgressPropertyItem): Progress item to be removed.
        """
        assert(isinstance(item, progress.ProgressPropertyItem))

        progress_items = getattr(bpy.context.window_manager, cls._attrname)
        for i, j in enumerate(progress_items):
            if item.index == j.index:
                progress_items.remove(i)

        if not len(progress_items):
            cls.release_all()

    @classmethod
    def release_all(cls):
        """Removes all progressbars"""
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
