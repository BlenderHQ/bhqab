import bpy

from .. import ui


class BHQABT_OT_Progress(bpy.types.Operator):
    bl_idname = "bhqabt.progress"
    bl_label = "Progress"
    bl_options = {'INTERNAL'}

    cancellable: bpy.props.BoolProperty()

    def execute(self, context):
        self._progress = ui.progress.invoke()
        self._progress.cancellable = self.cancellable
        self._progress.label = f"{self._progress.as_pointer()}"
        self._progress.icon = 'INFO'
        self._progress.num_steps = 50

        wm = context.window_manager
        wm.modal_handler_add(self)
        self._timer = wm.event_timer_add(time_step=0.1, window=context.window)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        ui.progress.complete(self._progress)

    def modal(self, context, event):
        if event.type == 'TIMER':
            self._progress.step += 1

        if self._progress.value >= 100.0 or (not self._progress.valid) or event.type == 'ESC':
            self.cancel(context)
            return {'FINISHED'}

        return {'PASS_THROUGH'}
