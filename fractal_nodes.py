from operator import truediv
import bpy
from bpy.types import Operator
from bpy.types import NodeSocket
from .utils import *


class FractalNodesOperators(Operator):
    bl_label = 'Fractal Nodes operators'
    bl_idname = 'op.fractal_nodes_operators'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(
        items=[
            ('CREATE_FRACTAL_NODES', 'create fractal nodes', 'create fractal nodes'),
        ]
    )

    def execute(self, context):
        if self.action == 'CREATE_FRACTAL_NODES':
            self.create_test_group(self, context=context)
        return {'FINISHED'}

    @staticmethod
    def create_test_group(self, context):
        # Add geo node to cube object
        obj = bpy.context.scene.objects['Cube']
        geo_mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        tree = geo_mod.node_group
        nodes = tree.nodes

        # for n in nodes:
        #     print(n.name, n)
        #group_input = tree.nodes.new("NodeGroupInput")

        # Get group input and output
        group_input = tree.nodes.get("Group Input")
        group_input.location = (-500, 0)
        group_outpout = tree.nodes.get("Group Output")

        # Add all outputs to the group input of the geometry node
        tree.inputs.new('NodeSocketInt', 'Instance Object Index 1')
        tree.inputs.new('NodeSocketInt', 'Instance Object Index 2')
        tree.inputs.new('NodeSocketInt', 'Instance Object Index 3')
        tree.inputs.new('NodeSocketInt', 'Instance Object Index 4')
        tree.inputs.new('NodeSocketVector', 'Rotation 1')
        tree.inputs.new('NodeSocketVector', 'Rotation 2')
        tree.inputs.new('NodeSocketVector', 'Rotation 3')
        tree.inputs.new('NodeSocketVector', 'Rotation 4')
        tree.inputs.new('NodeSocketFloat', 'Scale Factor 1')
        tree.inputs.new('NodeSocketFloat', 'Scale Factor 2')
        tree.inputs.new('NodeSocketFloat', 'Scale Factor 3')
        tree.inputs.new('NodeSocketFloat', 'Scale Factor 4')
        tree.inputs.new('NodeSocketVector', 'Scale Origin')

        # Add nodes
        # Classic GeoNodes
        fractal_geometry_node_transform = tree.nodes.new(
            "GeometryNodeTransform")
        fractal_geometry_node_transform = tree.nodes.new(
            "GeometryNodeJoinGeometry")
        fractal_geometry_node_transform = tree.nodes.new(
            "GeometryNodeRealizeInstances")
        fractal_geometry_node_transform = tree.nodes.new(
            "GeometryNodeCollectionInfo")

        # Fractal Iteration Nodes
        fractal_iteration_node_generator = self.generateFractalIterationNode()
        fractal_iteration_node1 = tree.nodes.new('GeometryNodeGroup')
        fractal_iteration_node1.node_tree = fractal_iteration_node_generator

        fractal_iteration_node2 = tree.nodes.new('GeometryNodeGroup')
        fractal_iteration_node2.node_tree = fractal_iteration_node_generator

        fractal_iteration_node3 = tree.nodes.new('GeometryNodeGroup')
        fractal_iteration_node3.node_tree = fractal_iteration_node_generator

        fractal_iteration_node4 = tree.nodes.new('GeometryNodeGroup')
        fractal_iteration_node4.node_tree = fractal_iteration_node_generator

        # Create new node instance on points
        # get names from subclasses https://docs.blender.org/api/current/bpy.types.GeometryNode.html#bpy.types.GeometryNode

        # Get inputs of node
        # print(nodeinputs)
        # for f in nodeinputs:
        #     print(f.identifier)

        # nodeinputsInstance = nodeinputs.get('Instance')

        # CREATE LINKS

        # Create function
        link = tree.links.new

        # Create input in input group
        # tree.inputs.new('NodeSocket')

        # link(group_input.outputs[0], nodeinputsInstance)

        # tree.interface_update(context)
        # https://docs.blender.org/api/current/bpy.types.NodeSocket.html#bpy.types.NodeSocket

        newGeom = group_input.outputs.new('GEOMETRY', 'new geo')
        newGeom.name = "hello"

        # nodeinputsPoints = nodeinputs.get('Points')

        # print(group_input.outputs)
        # for j in group_input.outputs:
        #     print(j.type)

    def generateFractalIterationNode(self):
        # CREATE FRACTAL ITERATION GROUP
        # Create the node group aka node tree
        fractal_iteration_group = bpy.data.node_groups.new(
            'Fractal Iteration Group', 'GeometryNodeTree')

        # Add NodeGroup Input and Output
        # Inputs
        fractal_iteration_group_input = fractal_iteration_group.nodes.new(
            "NodeGroupInput")
        fractal_iteration_group_input.location = (-500, 0)
        fractal_input_base = fractal_iteration_group.inputs.new(
            'NodeSocketFloat', 'Base')
        fractal_input_exponent = fractal_iteration_group.inputs.new(
            'NodeSocketFloat', 'Exponent')
        fractal_input_rotation = fractal_iteration_group.inputs.new(
            'NodeSocketVector', 'Rotation')
        fractal_input_points = fractal_iteration_group.inputs.new(
            'NodeSocketGeometry', 'Points')
        fractal_input_instance = fractal_iteration_group.inputs.new(
            'NodeSocketGeometry', 'Instance')
        fractal_input_index = fractal_iteration_group.inputs.new(
            'NodeSocketInt', 'Instance Index')

        # Outputs
        fractal_iteration_group_output = fractal_iteration_group.nodes.new(
            "NodeGroupOutput")
        fractal_iteration_group_output.location = (1000, 0)
        fractal_input_instance = fractal_iteration_group.outputs.new(
            'NodeSocketGeometry', 'Instance')

        # Add necessary nodes
        ## Separate / Combine
        fractal_separate = fractal_iteration_group.nodes.new(
            'ShaderNodeSeparateXYZ')
        fractal_separate.location = (-200, 150)
        fractal_combine = fractal_iteration_group.nodes.new(
            'ShaderNodeCombineXYZ')
        fractal_combine.location = (200, 150)

        # To Radians
        fractal_to_radians_1 = fractal_iteration_group.nodes.new(
            'ShaderNodeMath')
        fractal_to_radians_1.operation = 'RADIANS'
        fractal_to_radians_1.hide = True
        fractal_to_radians_1.location = (0, 200)

        fractal_to_radians_2 = fractal_iteration_group.nodes.new(
            'ShaderNodeMath')
        fractal_to_radians_2.operation = 'RADIANS'
        fractal_to_radians_2.hide = True
        fractal_to_radians_2.location = (0, 150)

        fractal_to_radians_3 = fractal_iteration_group.nodes.new(
            'ShaderNodeMath')
        fractal_to_radians_3.operation = 'RADIANS'
        fractal_to_radians_3.hide = True
        fractal_to_radians_3.location = (0, 100)

        # Instance on points
        fractal_instance_on_point = fractal_iteration_group.nodes.new(
            "GeometryNodeInstanceOnPoints")
        fractal_instance_on_point.inputs['Pick Instance'].default_value = True
        fractal_instance_on_point.location = (800, 0)

        # Power
        fractal_power = fractal_iteration_group.nodes.new(
            'ShaderNodeMath')
        fractal_power.operation = 'POWER'
        fractal_power.location = (-200, -300)

        # Combine 2
        fractal_combine2 = fractal_iteration_group.nodes.new(
            'ShaderNodeCombineXYZ')
        fractal_combine2.location = (200, -300)

        # Linking nodes
        linkGroup = fractal_iteration_group.links.new

        # Linking TO instance on points
        linkGroup(
            fractal_combine.outputs[0], fractal_instance_on_point.inputs['Rotation'])
        linkGroup(
            fractal_combine2.outputs[0], fractal_instance_on_point.inputs['Scale'])
        linkGroup(
            fractal_iteration_group_input.outputs['Points'], fractal_instance_on_point.inputs['Points'])
        linkGroup(
            fractal_iteration_group_input.outputs['Instance'], fractal_instance_on_point.inputs['Instance'])
        linkGroup(
            fractal_iteration_group_input.outputs['Instance Index'], fractal_instance_on_point.inputs['Instance Index'])

        # Linking FROM instance on points
        linkGroup(
            fractal_instance_on_point.outputs[0], fractal_iteration_group_output.inputs[0])

        # Linking Separate / Radians / Combine
        linkGroup(
            fractal_iteration_group_input.outputs['Rotation'], fractal_separate.inputs[0])

        linkGroup(
            fractal_separate.outputs['X'], fractal_to_radians_1.inputs[0])
        linkGroup(
            fractal_separate.outputs['Y'], fractal_to_radians_2.inputs[0])
        linkGroup(
            fractal_separate.outputs['Z'], fractal_to_radians_3.inputs[0])

        linkGroup(
            fractal_to_radians_1.outputs[0], fractal_combine.inputs['X'])
        linkGroup(
            fractal_to_radians_2.outputs[0], fractal_combine.inputs['Y'])
        linkGroup(
            fractal_to_radians_3.outputs[0], fractal_combine.inputs['Z'])

        # Linking power / combine
        linkGroup(
            fractal_iteration_group_input.outputs['Base'], fractal_power.inputs[0])
        linkGroup(
            fractal_iteration_group_input.outputs['Exponent'], fractal_power.inputs[1])

        linkGroup(fractal_power.outputs[0], fractal_combine2.inputs['X'])
        linkGroup(fractal_power.outputs[0], fractal_combine2.inputs['Y'])
        linkGroup(fractal_power.outputs[0], fractal_combine2.inputs['Z'])

        return fractal_iteration_group


def register():
    bpy.utils.register_class(FractalNodesOperators)


def unregister():
    bpy.utils.unregister_class(FractalNodesOperators)
