from operator import truediv
import bpy
from bpy.types import Operator, Scene
from .utils import *


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
             'compute next iteration', 'compute next iteration')
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
        return {'FINISHED'}

    @staticmethod
    def add_fractal_collection(context):
        collection = context.blend_data.collections.new(name='fractal')
        context.collection.children.link(collection)
        add_uv_sphere(collection)
        add_cube(collection)
        add_cone(collection)
        FractalOperators.fractals_pool.add(collection)
        FractalOperators.fractals_pool.select(collection)

    @staticmethod
    def remove_selected_fractal_collection(context):
        selected = context.collection
        FractalOperators.fractals_pool.remove(selected)

    @staticmethod
    def clear_all_fractal_collections(context):
        FractalOperators.fractals_pool.remove_all()

    @staticmethod
    def compute_next_iteration(context):
        print(context.scene.fractal_1_like)
        print(context.scene.fractal_2_like)
        print(context.scene.fractal_3_like)
        print(context.scene.fractal_4_like)
        reset_bool_properties(context)


def register():
    bpy.utils.register_class(FractalOperators)
    Scene.my_property = bpy.props.BoolProperty(default=True)


def unregister():
    bpy.utils.unregister_class(FractalOperators)
    del Scene.my_property
