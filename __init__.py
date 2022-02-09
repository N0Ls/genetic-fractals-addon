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

import bpy

def register():
    from . import properties
    from . import ui
    from . import utils
    properties.register()
    ui.register()
    utils.register()

def unregister():
    from . import properties
    from . import ui
    from . import utils
    properties.unregister()
    ui.unregister()
    utils.unregister()

if __name__ == '__main__':
    register()
