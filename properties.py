from operator import truediv
import bpy
from bpy.types import Operator, Scene
from .utils import *
from .fractal_nodes import *


class Fractal():
    bl_label = 'Fractal'
    bl_idname = 'cs.fractal'
    bl_description = ''

    def __init__(self, collection):
        self.container = collection
        self.value = 0

    def __del__(self):
        print("Fractal instance deleted")


class FractalPool():
    bl_label = 'Fractal pool'
    bl_idname = 'cs.fractal_pool'
    bl_description = ''

    def __init__(self):
        self.pool = []

    def add(self, collection):
        self.pool.append(Fractal(collection))

    def remove(self, collection):
        if self.exists(collection):
            self.__remove_linked_objects_of(collection)
            bpy.data.collections.remove(collection)
            fractal_to_remove = find_instance(
                lambda f: f.container == collection, self.pool)
            self.pool.remove(fractal_to_remove)

    def remove_all(self):
        for fractal in self.pool:
            self.__remove_linked_objects_of(fractal.container)
            bpy.data.collections.remove(fractal.container)
        self.pool = []

    def select(self, collection):
        layer_collection = bpy.context.view_layer.layer_collection
        layerColl = traverse_layer_collection(
            layer_collection, collection.name)
        bpy.context.view_layer.active_layer_collection = layerColl

    def exclude(self, collection):
        layer_collection = bpy.context.view_layer.layer_collection
        layerColl = traverse_layer_collection(
            layer_collection, collection.name)
        layerColl.exclude = True

    def exists(self, collection):
        return find_instance(lambda f: f.container == collection, self.pool)

    def __remove_linked_objects_of(self, collection):
        col = bpy.data.collections.get(collection.name)
        for object in col.objects:
            bpy.data.objects.remove(object, do_unlink=True)


class FractalOperators(Operator):
    bl_label = 'Fractal operator'
    bl_idname = 'op.fractal_operators'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(
        items=[
            ('ADD_FRACTAL_COLLECTION', 'add fractal collection',
             'add fractal collection'),
            ('REMOVE_SELECTED_FRACTAL_COLLECTION', 'remove selected fractal collection',
             'remove selected fractal collection'),
            ('CLEAR_ALL_FRACTAL_COLLECTIONS', 'clear all fractal collections',
             'clear all fractal collections'),
            ('COMPUTE_NEXT_ITERATION',
             'compute next iteration', 'compute next iteration'),
            ('GENERATE_FRACTAL_SETUP', 'generate all fractal setup',
             'generate all fractal setup')
        ]
    )

    fractals_pool = FractalPool()

    def execute(self, context):
        if self.action == 'ADD_FRACTAL_COLLECTION':
            self.add_fractal_collection(context=context)
        elif self.action == 'REMOVE_SELECTED_FRACTAL_COLLECTION':
            self.remove_selected_fractal_collection(context=context)
        elif self.action == 'CLEAR_ALL_FRACTAL_COLLECTIONS':
            self.clear_all_fractal_collections(context=context)
        elif self.action == 'COMPUTE_NEXT_ITERATION':
            self.compute_next_iteration(context=context)
        elif self.action == 'GENERATE_FRACTAL_SETUP':
            self.generate_fractal_setup(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_fractal_collection(context):
        collection = context.blend_data.collections.new(name='fractal')
        context.collection.children.link(collection)
        add_uv_sphere(collection)
        add_cube(collection)
        add_cone(collection)
        FractalOperators.fractals_pool.add(collection)
        FractalOperators.fractals_pool.exclude(collection)

    @staticmethod
    def remove_selected_fractal_collection(context):
        selected = context.collection
        FractalOperators.fractals_pool.remove(selected)

    @staticmethod
    def clear_all_fractal_collections(context):
        FractalOperators.fractals_pool.remove_all()

    @staticmethod
    def compute_next_iteration(context):
        print(round(context.scene.fractal_1_like, 2))
        print(round(context.scene.fractal_2_like, 2))
        print(round(context.scene.fractal_3_like, 2))
        print(round(context.scene.fractal_4_like, 2))
        reset_float_properties(context)

        obj = bpy.context.scene.objects["Fractal cube origin 1"]
        mod = obj.modifiers["GeometryNodes"]

        obj2 = bpy.context.scene.objects["Fractal cube origin 2"]
        mod2 = obj2.modifiers["GeometryNodes"]

        # binary_to_modifier(mod, modifier_to_binary(mod))
        binaryMod1 = modifier_to_binary(mod)
        binaryMod1 = mutation(binaryMod1, 0.1)
        binary_to_modifier(mod2, binaryMod1)

    @staticmethod
    def generate_fractal_setup(context):
        FractalOperators.add_fractal_collection(context=context)
        fractal_node_group = FractalNodesOperators.create_fractal_group(
            FractalNodesOperators, context=context, collection=context.blend_data.collections['fractal'])

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (5., 0., 0.)
        obj.name = 'Fractal cube origin 1'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group

        # Due to a bug we can't search by name of the input for now
        mod['Input_1'] = 0
        mod['Input_2'] = 1
        mod['Input_3'] = 5
        mod['Input_4'] = 8
        mod['Input_5'][0] = 45
        mod['Input_5'][1] = 45
        mod['Input_5'][2] = 45

        mod['Input_6'][0] = 33
        mod['Input_6'][1] = 48.5
        mod['Input_6'][2] = 75.3

        mod['Input_7'][0] = 87
        mod['Input_7'][1] = 90
        mod['Input_7'][2] = 23

        mod['Input_8'][0] = 48
        mod['Input_8'][1] = 36
        mod['Input_8'][2] = 12

        mod['Input_9'] = 1.32

        # for input in modifier.node_group.inputs:
        #     print(f"Input {input.identifier} is named {input.name}")

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (-5., 0., 0.)
        obj.name = 'Fractal cube origin 2'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (0., 5., 0.)
        obj.name = 'Fractal cube origin 3'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (0., -5., 0.)
        obj.name = 'Fractal cube origin 4'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group


def register():
    bpy.utils.register_class(FractalOperators)
    Scene.my_property = bpy.props.BoolProperty(default=True)


def unregister():
    bpy.utils.unregister_class(FractalOperators)
    del Scene.my_property
