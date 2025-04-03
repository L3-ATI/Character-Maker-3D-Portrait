bl_info = {
    "name": "Character 3D Portrait Maker",
    "description": "An add-on to customize a 3D portrait of a cartoon character.",
    "author": "Ton Nom",
    "version": (1, 0),
    "blender": (4, 3, 2),
    "location": "Vue 3D > N",
    "category": "3D View",
}

import bpy
import os

# Charger le script principal :
from . import mainScript

# Charger la scène au démarrage :
def load_scene():
    filepath = os.path.join(os.path.dirname(__file__), "mainScene.blend")
    bpy.ops.wm.open_mainfile(filepath=filepath)

# Fonction d’enregistrement
def register():
    mainScript.register()
    load_scene()

# Fonction de désenregistrement
def unregister():
    mainScript.unregister()

if __name__ == "__main__":
    register()
