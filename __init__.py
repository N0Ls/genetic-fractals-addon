bl_info = {
    "name": "Genetic fractals",
    "description": "Genetic algorithm powered fractals generator for Blender.",
    "author": "LANDRODIE Nils, SCAVINNER Vincent, DUVINAGE Evan-James, DESGOUTTES Baptiste",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N",
    "category": "View 3D",
    "warning": "",
}

import bpy
from . import properties
from . import ui
from . import utils
from . import fractal_nodes

def register():
    properties.register()
    ui.register()
    utils.register()
    fractal_nodes.register()


def unregister():
    properties.unregister()
    ui.unregister()
    utils.unregister()
    fractal_nodes.unregister()


if __name__ == '__main__':
    register()
