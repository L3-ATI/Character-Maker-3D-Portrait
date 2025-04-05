bl_info = {
    "name": "Character_3D_Portrait_Maker",
    "description": "Demo Character customizer in Blender.",
    "author": "Aconitum — Giulia Haut Perucca",
    "version": (1, 0),
    "blender": (4, 3, 2),
    "location": "Vue 3D > N",
    "category": "3D View",
}

import bpy
import os

# Charger le script principal
from . import mainScript

def register():
    mainScript.register()

def unregister():
    mainScript.unregister()

if __name__ == "__main__":
    register()
