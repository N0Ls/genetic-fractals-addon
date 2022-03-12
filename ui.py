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
        row1 = layout.row()
        row1.operator('op.fractal_operators',
                      text='Create fractal').action = 'ADD_FRACTAL_COLLECTION'
        row4 = layout.row()
        row4.operator('op.fractal_nodes_operators',
                      text='Create nodes').action = 'CREATE_FRACTAL_NODES'

        if FractalOperators.fractals_pool.exists(context.collection):
            row1.enabled = False
        if (len(FractalOperators.fractals_pool.pool)):
            row2 = layout.row()
            row2.operator('op.fractal_operators',
                          text='Clear all').action = 'CLEAR_ALL_FRACTAL_COLLECTIONS'
        if FractalOperators.fractals_pool.exists(context.collection):
            row3 = layout.row()
            row3.operator('op.fractal_operators',
                          text='Remove selected fractal').action = 'REMOVE_SELECTED_FRACTAL_COLLECTION'


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
