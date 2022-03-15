import bpy
from bpy.types import Panel
from bpy.props import BoolProperty, FloatProperty
from .properties import FractalOperators
from .fractal_nodes import FractalNodesOperators


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
        row0 = layout.row()
        row0.operator('op.fractal_operators',
                      text='Do some crazy stuff').action = 'GENERATE_FRACTAL_SETUP'

        if FractalOperators.fractals_pool.exists(context.collection):
            row0.enabled = False

        row2 = layout.row()
        row2.operator('op.fractal_operators',
                      text='Reset fractals').action = 'RESET_FRACTALS'

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
