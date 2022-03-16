from operator import truediv
import bpy
import os
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
             'generate all fractal setup'),
            ('RESET_FRACTALS', 'reset fractals', 'reset fractals'),
            ('EXPORT', 'export', 'export')
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
        elif self.action == 'RESET_FRACTALS':
            self.reset_fractals(context=context)
        elif self.action == 'EXPORT':
            self.export_to_file(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_fractal_collection(context):
        collection = context.blend_data.collections.new(name='fractal')
        context.collection.children.link(collection)
        add_cube(collection)
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
    def reset_fractals(context):
        # Getting modifiers
        obj1 = bpy.context.scene.objects["Fractal cube origin 1"]
        mod1 = obj1.modifiers["GeometryNodes"]

        obj2 = bpy.context.scene.objects["Fractal cube origin 2"]
        mod2 = obj2.modifiers["GeometryNodes"]

        obj3 = bpy.context.scene.objects["Fractal cube origin 3"]
        mod3 = obj3.modifiers["GeometryNodes"]

        obj4 = bpy.context.scene.objects["Fractal cube origin 4"]
        mod4 = obj4.modifiers["GeometryNodes"]

        randomGene1 = generateRandomGene()
        randomGene2 = generateRandomGene()
        randomGene3 = generateRandomGene()
        randomGene4 = generateRandomGene()

        binary_to_modifier(mod1, randomGene1)
        binary_to_modifier(mod2, randomGene2)
        binary_to_modifier(mod3, randomGene3)
        binary_to_modifier(mod4, randomGene4)

    @staticmethod
    def compute_next_iteration(context):

        # Getting modifiers
        obj1 = bpy.context.scene.objects["Fractal cube origin 1"]
        mod1 = obj1.modifiers["GeometryNodes"]

        obj2 = bpy.context.scene.objects["Fractal cube origin 2"]
        mod2 = obj2.modifiers["GeometryNodes"]

        obj3 = bpy.context.scene.objects["Fractal cube origin 3"]
        mod3 = obj3.modifiers["GeometryNodes"]

        obj4 = bpy.context.scene.objects["Fractal cube origin 4"]
        mod4 = obj4.modifiers["GeometryNodes"]

        fitness1 = round(context.scene.fractal_1_like, 2)
        fitness2 = round(context.scene.fractal_2_like, 2)
        fitness3 = round(context.scene.fractal_3_like, 2)
        fitness4 = round(context.scene.fractal_4_like, 2)

        # Parents selection
        parent1 = modifier_to_binary(mod1)
        parent2 = modifier_to_binary(mod2)
        parent3 = modifier_to_binary(mod3)
        parent4 = modifier_to_binary(mod4)

        if(random.random() > fitness1):
            parent1 = crossover(parent3, parent4, 1.0)[0]

        if(random.random() > fitness2):
            parent2 = crossover(parent1, parent3, 1.0)[0]

        if(random.random() > fitness3):
            parent3 = crossover(parent1, parent2, 1.0)[0]

        if(random.random() > fitness4):
            parent4 = crossover(parent2, parent3, 1.0)[0]

        # reset_float_properties(context)

        # Reproduction
        # faire un truc ou ça selectionne en fonction du fitness ?
        [child1, child2] = crossover(
            parent1=parent1, parent2=parent2, cross_rate=0.07)
        [child3, child4] = crossover(
            parent1=parent3, parent2=parent4, cross_rate=0.07)

        # Mutation
        child1 = mutation(child1, context.scene.mutation_rate)
        child2 = mutation(child2, context.scene.mutation_rate)
        child3 = mutation(child3, context.scene.mutation_rate)
        child4 = mutation(child4, context.scene.mutation_rate)

        # Apply modifers
        binary_to_modifier(mod1, child1)
        binary_to_modifier(mod2, child2)
        binary_to_modifier(mod3, child3)
        binary_to_modifier(mod4, child4)

    @staticmethod
    def generate_fractal_setup(context):
        FractalOperators.add_fractal_collection(context=context)
        fractal_node_group = FractalNodesOperators.create_fractal_group(
            FractalNodesOperators, context=context, collection=context.blend_data.collections['fractal'])

        randomGene1 = generateRandomGene()
        randomGene2 = generateRandomGene()
        randomGene3 = generateRandomGene()
        randomGene4 = generateRandomGene()

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (5., 0., 0.)
        obj.name = 'Fractal cube origin 1'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group
        binary_to_modifier(mod, randomGene1)

        # for input in modifier.node_group.inputs:
        #     print(f"Input {input.identifier} is named {input.name}")

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (-5., 0., 0.)
        obj.name = 'Fractal cube origin 2'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group
        binary_to_modifier(mod, randomGene2)

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (0., 5., 0.)
        obj.name = 'Fractal cube origin 3'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group
        binary_to_modifier(mod, randomGene3)

        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.location = (0., -5., 0.)
        obj.name = 'Fractal cube origin 4'
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        mod.node_group = fractal_node_group
        binary_to_modifier(mod, randomGene4)

    @staticmethod
    def export_to_file(context):
        path = context.scene.filepath
        os.makedirs(path, exist_ok=True)

        # Write data out (2 integers)
        with open(path + "file.txt", "w") as file:
            # Getting modifiers
            obj1 = bpy.context.scene.objects["Fractal cube origin 1"]
            mod1 = obj1.modifiers["GeometryNodes"]

            obj2 = bpy.context.scene.objects["Fractal cube origin 2"]
            mod2 = obj2.modifiers["GeometryNodes"]

            obj3 = bpy.context.scene.objects["Fractal cube origin 3"]
            mod3 = obj3.modifiers["GeometryNodes"]

            obj4 = bpy.context.scene.objects["Fractal cube origin 4"]
            mod4 = obj4.modifiers["GeometryNodes"]
            file.write(modifier_to_binary(mod1) + '\n')
            file.write(modifier_to_binary(mod2) + '\n')
            file.write(modifier_to_binary(mod3) + '\n')
            file.write(modifier_to_binary(mod4) + '\n')
            file.close()


def register():
    bpy.utils.register_class(FractalOperators)
    Scene.my_property = bpy.props.BoolProperty(default=True)


def unregister():
    bpy.utils.unregister_class(FractalOperators)
    del Scene.my_property
