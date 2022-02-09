import bpy

def find_instance(fn, objs):
    all_matches = list(filter(fn, objs))
    return len(all_matches) > 0 and all_matches[0] 

def traverse_layer_collection(layer_collection, name_to_found):
        found = None
        if (layer_collection.name == name_to_found):
            return layer_collection
        for layer in layer_collection.children:
            found = traverse_layer_collection(layer, name_to_found)
            if found:
                return found

def add_uv_sphere(collection):
    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)

def add_cube(collection):
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)

def add_cone(collection):
    bpy.ops.mesh.primitive_cone_add()
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[collection.name].objects.link(obj)

def register():
    pass

def unregister():
    pass