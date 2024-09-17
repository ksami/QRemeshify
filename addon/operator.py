import bpy
from bpy.types import Operator, Context
from .lib import main


class QUADWILD_OT_REMESH(Operator):
    """Remesh with Quadwild"""
    bl_idname = "quadwild.remesh"
    bl_label = "Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        row = self.layout
        row.progress(self, type='RING', factor=0.7, text="Running...")

    def execute(self, ctx: Context):
        main('example/suzanne.obj')
        return {'FINISHED'}
