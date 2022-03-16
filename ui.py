import bpy
import os
from bpy.types import Panel
from bpy.props import FloatProperty, StringProperty
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

        row2 = layout.row()
        row2.operator('op.fractal_operators',
                      text='Reset fractals').action = 'RESET_FRACTALS'


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

bpy.types.Scene.filepath = StringProperty(
    name="filepath",
    description="Some tooltip",
    default='//', subtype='FILE_PATH')


class GeneticPanel(Panel):
    bl_label = "Genetic"
    bl_idname = "pt.genetic_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fractal'

    def draw(self, context):
        layout = self.layout
        sceneCtx = context.scene

        layout.prop(sceneCtx, "fractal_1_like")
        layout.prop(sceneCtx, "fractal_2_like")
        layout.prop(sceneCtx, "fractal_3_like")
        layout.prop(sceneCtx, "fractal_4_like")

        layout.separator()

        nextItRow = layout.row()
        nextItRow.operator('op.fractal_operators',
                           text='Compute next iteration').action = 'COMPUTE_NEXT_ITERATION'


class ExportPanel(Panel):
    bl_label = "Export"
    bl_idname = "pt.export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fractal'

    def draw(self, context):
        layout = self.layout
        sceneCtx = context.scene

        layout.prop(sceneCtx, "filepath")
        layout.operator("object.filepath")

        exportButtonRow = layout.row()
        exportButtonRow.operator('op.fractal_operators',
                                 text='Export').action = 'EXPORT'


def register():
    bpy.utils.register_class(GenerationPanel)
    bpy.utils.register_class(GeneticPanel)
    bpy.utils.register_class(ExportPanel)


def unregister():
    bpy.utils.unregister_class(GenerationPanel)
    bpy.utils.unregister_class(GeneticPanel)
    bpy.utils.unregister_class(ExportPanel)
