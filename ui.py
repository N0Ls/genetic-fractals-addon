import bpy
from bpy.types import Panel
from bpy.props import BoolProperty, FloatProperty
from .properties import FractalOperators

bpy.types.Scene.fractal_1_like = FloatProperty(
    name="Fractal 1",
    description="Some tooltip",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_2_like = FloatProperty(
    name="Fractal 2",
    description="Some tooltip",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_3_like = FloatProperty(
    name="Fractal 3",
    description="Some tooltip",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_4_like = FloatProperty(
    name="Fractal 4",
    description="Some tooltip",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)


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
        row4 = layout.row()
        row4.operator('op.fractal_operators',
                      text='Next iteration').action = 'COMPUTE_NEXT_ITERATION'


class PropertiesPanel(Panel):
    bl_label = "Properties"
    bl_idname = "pt.properties_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fractal'

    def draw(self, context):
        layout = self.layout
        sceneCtx = context.scene
        # draw the checkbox (implied from property type = bool)
        layout.prop(sceneCtx, "fractal_1_like")
        layout.prop(sceneCtx, "fractal_2_like")
        layout.prop(sceneCtx, "fractal_3_like")
        layout.prop(sceneCtx, "fractal_4_like")


def register():
    bpy.utils.register_class(GenerationPanel)
    bpy.utils.register_class(PropertiesPanel)


def unregister():
    bpy.utils.unregister_class(GenerationPanel)
    bpy.utils.unregister_class(PropertiesPanel)
