import bpy
bl_info = {
    "name": "Genetic fractals",
    "description": "Algo genetic powered fractals generator for Blender.",
    "author": "",
    "version": (1, 0),
    "blender": (3, 0, 1),
    "location": "",
    "warning": "This version is still a work in progress.",
    "wiki_url": "",
    "tracker_url": "",
    "support": "",
    "category": ""
}


def register():
    from . import properties
    from . import ui
    from . import utils
    from . import fractal_nodes
    properties.register()
    ui.register()
    utils.register()
    fractal_nodes.register()


def unregister():
    from . import properties
    from . import ui
    from . import utils
    from . import fractal_nodes
    properties.unregister()
    ui.unregister()
    utils.unregister()
    fractal_nodes.unregister()


if __name__ == '__main__':
    register()
