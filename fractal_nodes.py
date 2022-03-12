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
            collection = context.blend_data.collections.new(name='test')
            self.create_fractal_group(self, context=context,
                                      collection=collection)
        return {'FINISHED'}

    @staticmethod
    def create_fractal_group(self, context, collection):
        # Add geo node to cube object

        fractal_group = bpy.data.node_groups.new(
            'Fractal Group', 'GeometryNodeTree')
        nodes = fractal_group.nodes

        # for n in nodes:
        #     print(n.name, n)
        #group_input = fractal_group.nodes.new("NodeGroupInput")

        # Get group input and output
        group_input = fractal_group.nodes.new(
            "NodeGroupInput")
        group_input.location = (-1000, 0)
        group_output = fractal_group.nodes.new(
            "NodeGroupOutput")
        group_output.location = (1000, 0)

        # Add all outputs to the group input of the geometry node
        fractal_geometry_node_index1 = fractal_group.inputs.new(
            'NodeSocketGeometry', 'Geometry')
        fractal_geometry_node_index1 = fractal_group.inputs.new(
            'NodeSocketInt', 'Instance Object Index 1')
        fractal_geometry_node_index2 = fractal_group.inputs.new(
            'NodeSocketInt', 'Instance Object Index 2')
        fractal_geometry_node_index3 = fractal_group.inputs.new(
            'NodeSocketInt', 'Instance Object Index 3')
        fractal_geometry_node_index4 = fractal_group.inputs.new(
            'NodeSocketInt', 'Instance Object Index 4')
        fractal_geometry_node_rotation1 = fractal_group.inputs.new(
            'NodeSocketVector', 'Rotation 1')
        fractal_geometry_node_rotation2 = fractal_group.inputs.new(
            'NodeSocketVector', 'Rotation 2')
        fractal_geometry_node_rotation3 = fractal_group.inputs.new(
            'NodeSocketVector', 'Rotation 3')
        fractal_geometry_node_rotation4 = fractal_group.inputs.new(
            'NodeSocketVector', 'Rotation 4')
        fractal_geometry_node_scale1 = fractal_group.inputs.new(
            'NodeSocketFloat', 'Scale Factor 1')
        fractal_geometry_node_scale2 = fractal_group.inputs.new(
            'NodeSocketFloat', 'Scale Factor 2')
        fractal_geometry_node_scale3 = fractal_group.inputs.new(
            'NodeSocketFloat', 'Scale Factor 3')
        fractal_geometry_node_scale4 = fractal_group.inputs.new(
            'NodeSocketFloat', 'Scale Factor 4')
        fractal_geometry_node_scaleOrigin = fractal_group.inputs.new(
            'NodeSocketVector', 'Scale Origin')

        # Set default values
        default_scale_value = 0.4
        default_min_value = 0.0
        default_max_value = 2.0

        fractal_geometry_node_scale1.default_value = default_scale_value
        fractal_geometry_node_scale1.min_value = default_min_value
        fractal_geometry_node_scale1.max_value = default_max_value

        fractal_geometry_node_scale2.default_value = default_scale_value
        fractal_geometry_node_scale2.min_value = default_min_value
        fractal_geometry_node_scale2.max_value = default_max_value

        fractal_geometry_node_scale3.default_value = default_scale_value
        fractal_geometry_node_scale3.min_value = default_min_value
        fractal_geometry_node_scale3.max_value = default_max_value

        fractal_geometry_node_scale4.default_value = default_scale_value
        fractal_geometry_node_scale4.min_value = default_min_value
        fractal_geometry_node_scale4.max_value = default_max_value

        fractal_geometry_node_scaleOrigin.default_value = (1.0, 1.0, 1.0)

        # Add nodes
        # Classic GeoNodes
        fractal_geometry_node_transform = fractal_group.nodes.new(
            "GeometryNodeTransform")
        fractal_geometry_node_join = fractal_group.nodes.new(
            "GeometryNodeJoinGeometry")
        fractal_geometry_node_realize = fractal_group.nodes.new(
            "GeometryNodeRealizeInstances")
        fractal_geometry_node_collection = fractal_group.nodes.new(
            "GeometryNodeCollectionInfo")

        fractal_geometry_node_collection.inputs['Separate Children'].default_value = True
        fractal_geometry_node_collection.inputs['Reset Children'].default_value = True
        fractal_geometry_node_collection.inputs[0].default_value = collection

        fractal_geometry_node_collection.location = (-700, -420)
        fractal_geometry_node_realize.location = (775, 0)
        fractal_geometry_node_realize.hide = True
        fractal_geometry_node_join.location = (550, 0)
        fractal_geometry_node_join.hide = True
        fractal_geometry_node_transform.location = (-500, 0)
        fractal_geometry_node_transform.hide = True

        # Fractal Iteration Nodes
        fractal_iteration_node_generator = self.generateFractalIterationNode()
        fractal_iteration_node1 = fractal_group.nodes.new('GeometryNodeGroup')
        fractal_iteration_node1.node_tree = fractal_iteration_node_generator
        fractal_iteration_node1.location = (-320, 25)

        fractal_iteration_node2 = fractal_group.nodes.new('GeometryNodeGroup')
        fractal_iteration_node2.node_tree = fractal_iteration_node_generator
        fractal_iteration_node2.location = (-130, -50)

        fractal_iteration_node3 = fractal_group.nodes.new('GeometryNodeGroup')
        fractal_iteration_node3.node_tree = fractal_iteration_node_generator
        fractal_iteration_node3.location = (65, -160)

        fractal_iteration_node4 = fractal_group.nodes.new('GeometryNodeGroup')
        fractal_iteration_node4.node_tree = fractal_iteration_node_generator
        fractal_iteration_node4.location = (250, -250)

        # Links nodes
        # Create link function
        link = fractal_group.links.new

        link(group_input.outputs['Geometry'],
             fractal_geometry_node_transform.inputs['Geometry'])
        link(group_input.outputs['Scale Origin'],
             fractal_geometry_node_transform.inputs['Scale'])

        # Links TO join geometry
        link(
            fractal_geometry_node_transform.outputs['Geometry'], fractal_geometry_node_join.inputs[0])
        link(fractal_iteration_node1.outputs['Instance'],
             fractal_geometry_node_join.inputs[0])
        link(fractal_iteration_node2.outputs['Instance'],
             fractal_geometry_node_join.inputs[0])
        link(fractal_iteration_node3.outputs['Instance'],
             fractal_geometry_node_join.inputs[0])

        # Link realize
        link(fractal_geometry_node_join.outputs[0],
             fractal_geometry_node_realize.inputs[0])

        # Link to output
        link(fractal_geometry_node_realize.outputs[0], group_output.inputs[0])

        # Links TO iteration nodes
        link(group_input.outputs['Scale Factor 1'],
             fractal_iteration_node1.inputs['Base'])
        link(group_input.outputs['Rotation 1'],
             fractal_iteration_node1.inputs['Rotation'])
        link(group_input.outputs['Instance Object Index 1'],
             fractal_iteration_node1.inputs['Instance Index'])
        link(fractal_geometry_node_collection.outputs['Geometry'],
             fractal_iteration_node1.inputs['Instance'])
        link(fractal_geometry_node_transform.outputs['Geometry'],
             fractal_iteration_node1.inputs['Points'])

        link(group_input.outputs['Scale Factor 2'],
             fractal_iteration_node2.inputs['Base'])
        link(group_input.outputs['Rotation 2'],
             fractal_iteration_node2.inputs['Rotation'])
        link(group_input.outputs['Instance Object Index 2'],
             fractal_iteration_node2.inputs['Instance Index'])
        link(fractal_geometry_node_collection.outputs['Geometry'],
             fractal_iteration_node2.inputs['Instance'])
        link(fractal_iteration_node1.outputs['Instance'],
             fractal_iteration_node2.inputs['Points'])

        link(group_input.outputs['Scale Factor 3'],
             fractal_iteration_node3.inputs['Base'])
        link(group_input.outputs['Rotation 3'],
             fractal_iteration_node3.inputs['Rotation'])
        link(group_input.outputs['Instance Object Index 3'],
             fractal_iteration_node3.inputs['Instance Index'])
        link(fractal_geometry_node_collection.outputs['Geometry'],
             fractal_iteration_node3.inputs['Instance'])
        link(fractal_iteration_node2.outputs['Instance'],
             fractal_iteration_node3.inputs['Points'])

        link(group_input.outputs['Scale Factor 4'],
             fractal_iteration_node4.inputs['Base'])
        link(group_input.outputs['Rotation 4'],
             fractal_iteration_node4.inputs['Rotation'])
        link(group_input.outputs['Instance Object Index 4'],
             fractal_iteration_node4.inputs['Instance Index'])
        link(fractal_geometry_node_collection.outputs['Geometry'],
             fractal_iteration_node4.inputs['Instance'])
        link(fractal_iteration_node3.outputs['Instance'],
             fractal_iteration_node4.inputs['Points'])

        # Create new node instance on points
        # get names from subclasses https://docs.blender.org/api/current/bpy.types.GeometryNode.html#bpy.types.GeometryNode

        # Get inputs of node
        # print(nodeinputs)
        # for f in nodeinputs:
        #     print(f.identifier)

        # nodeinputsInstance = nodeinputs.get('Instance')

        # Create input in input group
        # fractal_group.inputs.new('NodeSocket')

        # link(group_input.outputs[0], nodeinputsInstance)

        # fractal_group.interface_update(context)
        # https://docs.blender.org/api/current/bpy.types.NodeSocket.html#bpy.types.NodeSocket

        # nodeinputsPoints = nodeinputs.get('Points')

        # print(group_input.outputs)
        # for j in group_input.outputs:
        #     print(j.type)

        return fractal_group

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

        fractal_input_exponent.default_value = 1.0

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
