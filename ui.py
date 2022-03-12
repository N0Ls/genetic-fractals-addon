import bpy
from bpy.types import Panel
from .properties import FractalOperators
from .fractal_nodes import FractalNodesOperators


class GenerationPanel(Panel):
    bl_label = "Generation"
    bl_idname = "pt.generation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fractal'

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        row0.operator('op.fractal_operators',
                      text='Do some crazy stuff').action = 'GENERATE_FRACTAL_SETUP'

        if FractalOperators.fractals_pool.exists(context.collection):
            row0.enabled = False


class PropertiesPanel(Panel):
    bl_label = "Properties"
    bl_idname = "pt.properties_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fractal'

    def draw(self, context):
        layout = self.layout


def register():
    bpy.utils.register_class(GenerationPanel)
    bpy.utils.register_class(PropertiesPanel)


def unregister():
    bpy.utils.unregister_class(GenerationPanel)
    bpy.utils.unregister_class(PropertiesPanel)
