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
        generateRow = layout.row()
        generateOperator = generateRow.operator('op.fractal_operators',
                      text='Generate setup')
        generateOperator.action = 'GENERATE_FRACTAL_SETUP'
        generateOperator.arg = 'generating the setup'

        if FractalOperators.fractals_pool.exists(context.collection):
            generateRow.enabled = False

        resetRow = layout.row()
        resetOperator = resetRow.operator('op.fractal_operators',
                      text='Reset fractals')
        resetOperator.action = 'RESET_FRACTALS'
        resetOperator.arg = 'reseting the fractals'


bpy.types.Scene.fractal_1_like = FloatProperty(
    name="Fractal 1 fitness",
    description="The fitness that will determine the survival of the fractal 1",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_2_like = FloatProperty(
    name="Fractal 2 fitness",
    description="The fitness that will determine the survival of the fractal 2",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_3_like = FloatProperty(
    name="Fractal 3 fitness",
    description="The fitness that will determine the survival of the fractal 3",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.fractal_4_like = FloatProperty(
    name="Fractal 4 fitness",
    description="The fitness that will determine the survival of the fractal 4",
    default=0.00,
    min=0.0, max=1.0, step=1, precision=2)

bpy.types.Scene.filepath = StringProperty(
    name="filepath",
    description="Some tooltip",
    default='//', subtype='FILE_PATH')

bpy.types.Scene.mutation_rate = FloatProperty(
    name="Mutation rate",
    description="Some tooltip",
    default=0.001,
    min=0.0, max=1.0, step=0.1, precision=4)


bpy.types.Scene.crossover_rate = FloatProperty(
    name="Crossover rate",
    description="Some tooltip",
    default=0.07,
    min=0.0, max=1.0, step=0.1, precision=4)


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
        layout.prop(sceneCtx, "mutation_rate")
        layout.prop(sceneCtx, "crossover_rate")

        layout.separator()

        nextItRow = layout.row()
        nextItOperator = nextItRow.operator('op.fractal_operators',
                           text='Compute next iteration')
        nextItOperator.action = 'COMPUTE_NEXT_ITERATION'
        nextItOperator.arg = 'computing the next iteration (generation) of the genetic algorithm'
        


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
        exportButtonOperator = exportButtonRow.operator('op.fractal_operators',
                                 text='Export')
        exportButtonOperator.action = 'EXPORT'
        exportButtonOperator.arg = 'exporting the genome'


def register():
    bpy.utils.register_class(GenerationPanel)
    bpy.utils.register_class(GeneticPanel)
    bpy.utils.register_class(ExportPanel)


def unregister():
    bpy.utils.unregister_class(GenerationPanel)
    bpy.utils.unregister_class(GeneticPanel)
    bpy.utils.unregister_class(ExportPanel)
