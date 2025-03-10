import bpy

def update_ear_type(self, context):
    """ Met à jour l'objet du modificateur Boolean de 'head' et les boucles d'oreilles en fonction du choix d'oreille et de boucle d'oreille """
    obj = bpy.data.objects.get("head")  # Récupérer l'objet 'head'
    
    if not obj:
        print("L'objet 'head' n'existe pas !")
        return
    
    # Vérifier si un modificateur Boolean est déjà présent
    bool_modifier = None
    for mod in obj.modifiers:
        if mod.type == 'BOOLEAN':
            bool_modifier = mod
            break
    
    if not bool_modifier:
        print("Aucun modificateur Boolean trouvé sur 'head'.")
        return
    
    # Associer l'oreille sélectionnée à un objet
    ear_objects = {
        "human": "boolEars1",
        "elfe": "boolEars2",
        "fae": "boolEars3"
    }
    
    selected_ear = ear_objects.get(self.ear_type, None)
    
    if selected_ear:
        ear_obj = bpy.data.objects.get(selected_ear)
        if ear_obj:
            bool_modifier.object = ear_obj
            print(f"Modificateur Boolean mis à jour avec {selected_ear}.")
        else:
            print(f"L'objet {selected_ear} n'existe pas dans la scène.")
    
    # Mise à jour des boucles d'oreilles en fonction du type d'oreilles et du type de boucle d'oreille
    earring_objects = {
        "human": {
            "stud": "studEarrings1",
            "hoop": "hoopEarrings1",
            "drop": "dropEarrings1"
        },
        "elfe": {
            "stud": "studEarrings2",
            "hoop": "hoopEarrings2",
            "drop": "dropEarrings2"
        },
        "fae": {
            "stud": "studEarrings3",
            "hoop": "hoopEarrings3",
            "drop": "dropEarrings3"
        }
    }
    
    # Désactiver toutes les boucles d'oreilles avant de les mettre à jour
    for obj in bpy.data.objects:
        if "Earrings" in obj.name:
            obj.hide_set(True)  # Cache les autres objets de boucles d'oreilles
    
    selected_earring = earring_objects.get(self.ear_type, {}).get(self.earrings, None)
    
    if selected_earring:
        earring_obj = bpy.data.objects.get(selected_earring)
        if earring_obj:
            earring_obj.hide_set(False)  # Affiche l'objet de boucles d'oreilles correspondant
            print(f"Modèle de boucles d'oreilles mis à jour avec {selected_earring}.")
        else:
            print(f"L'objet {selected_earring} n'existe pas dans la scène.")

def update_facial_shape_keys(self, context):
    """ Met à jour les shape keys du visage et des yeux en même temps. """
    head = bpy.data.objects.get("head")
    eyes = bpy.data.objects.get("eyes")  # Assure-toi que "eyes" est bien le nom de ton objet yeux

    if not head or not head.data.shape_keys:
        print("L'objet 'head' n'a pas de shape keys !")
        return

    if not eyes or not eyes.data.shape_keys:
        print("L'objet 'eyes' n'a pas de shape keys !")
        return

    # Shape keys associées
    shape_keys = {
    
        "brows_height": self.brows_height,
        "brows_depth": self.brows_depth,
        
        "eyes_proximity": self.eyes_proximity,
        "eyes_height": self.eyes_height,
        "eyes_size": self.eyes_size,
        "eyes_width": self.eyes_width,
        "eyes_length": self.eyes_length,
        "eyes_tilt": self.eyes_tilt,
        "eyes_closing": self.eyes_closing,
        
        "cheeks_proximity": self.cheeks_proximity,
        "cheeks_height": self.cheeks_height,
        "cheeks_size": self.cheeks_size,
        "cheeks_width": self.cheeks_width,
        "jaw_depth": self.jaw_depth,
        
        "nose_height": self.nose_height,
        "nose_width": self.nose_width,
        "nose_angle": self.nose_angle,
        
        "chin_size": self.chin_size,
        "chin_height": self.chin_height,
    }

    # Appliquer les valeurs aux shape keys du head
    for key, value in shape_keys.items():
        if key in head.data.shape_keys.key_blocks:
            head.data.shape_keys.key_blocks[key].value = value
        else:
            print(f"⚠️ Shape Key '{key}' non trouvée sur 'head'.")

        # Appliquer la valeur aux yeux uniquement si la shape key existe aussi sur eux
        if key in eyes.data.shape_keys.key_blocks:
            eyes.data.shape_keys.key_blocks[key].value = value
        else:
            print(f"⚠️ Shape Key '{key}' non trouvée sur 'eyes'. Ignorée.")

def update_hair_base(self, context):
    """ Active ou désactive les bangs dans le modificateur Boolean du hairBase """
    hair_objects = {
        "hb1": "hairBase1",
        "hb2": "hairBase2",
        "hb3": "hairBase3",
        "hb4": "hairBase4",
    }

    bangs_objects = {
        "boolBangs1": "boolBangs1",
        "boolBangs2": "boolBangs2",
        "boolBangs3": "boolBangs3",
        "boolBangs4": "boolBangs4",
    }

    # Parcourir tous les hairBase et leur appliquer le modificateur Boolean avec les bangs
    selected_bangs = bangs_objects.get(self.bangs, None)

    # Vérifie chaque hairBase et met à jour son modificateur Boolean
    for key, obj_name in hair_objects.items():
        if obj_name:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                # Chercher le modificateur Boolean sur l'objet
                bool_modifier = None
                for mod in obj.modifiers:
                    if mod.type == 'BOOLEAN' and mod.name == "BooleanBangs":  # Recherche le modificateur existant
                        bool_modifier = mod
                        break
                
                # Si un modificateur Boolean est trouvé, l'assigner au bon objet de bangs
                if bool_modifier:
                    bool_modifier.show_viewport = True  # Assurer que le modificateur est visible
                    if selected_bangs:
                        bool_modifier.object = bpy.data.objects.get(selected_bangs)
                    else:
                        bool_modifier.object = None  # Si aucun bangs sélectionné, ne rien affecter
                    print(f"Modificateur Boolean de {obj_name} mis à jour avec {selected_bangs}.")
       
    for key in hair_objects:
        obj_name = hair_objects[key]
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.hide_set(obj_name != self.hair_base)
       
class BUSTE_PT_CustomizerPanel(bpy.types.Panel):
    bl_label = "Character Maker 3D Portrait"
    bl_idname = "BUSTE_PT_CustomizerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Character Maker"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.buste_customizer
        
        # Hair options
        box = layout.box()
        box.label(text="Hair Settings")
        box.prop(props, "hair_base", text="Base")
        box.prop(props, "bangs", text="Bangs")
        
        # Ears options
        box = layout.box()
        box.label(text="Ear Settings")
        box.prop(props, "ear_type", text="Type")
        box.prop(props, "earrings", text="Earrings")
        
        # Eyes options
        box = layout.box()
        box.label(text="Eye Settings")
        box.prop(props, "eyelashes", text="Eyelashes")
        box.prop(props, "eye_shape", text="Shape")
        box.prop(props, "pupil_texture", text="Pupil Texture")
        
        # Shape Key sliders - eyes
        box.label(text="Brows Shape Adjustments")
        box.prop(props, "brows_height", text="Brow Height")
        box.prop(props, "brows_depth", text="Brow Depth")
        
        # Shape Key sliders - eyes
        box.label(text="Eye Shape Adjustments")
        box.prop(props, "eyes_proximity", text="Proximity")
        box.prop(props, "eyes_height", text="Height")
        box.prop(props, "eyes_size", text="Size")
        box.prop(props, "eyes_width", text="Width")
        box.prop(props, "eyes_length", text="Length")
        box.prop(props, "eyes_tilt", text="Tilt")
        box.prop(props, "eyes_closing", text="Closing")
        
        # Shape Key sliders - cheeks
        box.label(text="Cheeks Shape Adjustments")
        box.prop(props, "cheeks_proximity", text="Cheeks Proximity")
        box.prop(props, "cheeks_height", text="Cheeks Height")
        box.prop(props, "cheeks_size", text="Cheeks Size")
        box.prop(props, "cheeks_width", text="Cheeks Width")
        box.prop(props, "jaw_depth", text="Jaw Depth")
        
        # Shape Key sliders - nose
        box.label(text="Nose Shape Adjustments")
        box.prop(props, "nose_height", text="Nose Height")
        box.prop(props, "nose_width", text="Nose Width")
        box.prop(props, "nose_angle", text="Nose Angle")
        
        # Shape Key sliders - chin
        box.label(text="Chin Shape Adjustments")
        box.prop(props, "chin_size", text="Chin Size")
        box.prop(props, "chin_height", text="Chin Height")
        
        # Mouth options
        box = layout.box()
        box.label(text="Mouth Settings")
        box.prop(props, "mouth_texture", text="Texture")

class BUSTE_CustomizerProperties(bpy.types.PropertyGroup):
    # New shape keys for facial features
    brows_height: bpy.props.FloatProperty(
        name="Brow Height",
        description="Adjust the height of the eyebrows",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )
    
    brows_depth: bpy.props.FloatProperty(
        name="Brow Depth",
        description="Adjust how deep the brows are",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_proximity: bpy.props.FloatProperty(
        name="Eyes Proximity",
        description="Adjust distance between eyes",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_height: bpy.props.FloatProperty(
        name="Eyes Height",
        description="Adjust vertical eye position",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_size: bpy.props.FloatProperty(
        name="Eyes Size",
        description="Adjust overall eye size",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_width: bpy.props.FloatProperty(
        name="Eyes Width",
        description="Adjust eye width",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_length: bpy.props.FloatProperty(
        name="Eyes Length",
        description="Adjust eye length",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_tilt: bpy.props.FloatProperty(
        name="Eyes Tilt",
        description="Tilt the eyes",
        min=0.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    eyes_closing: bpy.props.FloatProperty(
        name="Eyes Closing",
        description="Control eyelid closure",
        min=0.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    # New properties for other facial features
    cheeks_proximity: bpy.props.FloatProperty(
        name="Cheeks Proximity",
        description="Adjust the proximity of the cheeks",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )
    
    cheeks_height: bpy.props.FloatProperty(
        name="Cheeks Height",
        description="Adjust the height of the cheeks",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )
    
    cheeks_size: bpy.props.FloatProperty(
        name="Cheeks Size",
        description="Adjust the size of the cheeks",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )
    
    cheeks_width: bpy.props.FloatProperty(
        name="Cheeks Width",
        description="Adjust the width of the cheeks",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )
    
    jaw_depth: bpy.props.FloatProperty(
        name="Jaw Depth",
        description="Adjust the depth of the jaw",
        min=-1.0, max=1.0, default=0.0,
        update=lambda self, context: update_facial_shape_keys(self, context)
    )

    hair_base: bpy.props.EnumProperty(
        name="Base Hair",
        items=[
            ("hb1", "Classic", "Classic hair base"),
            ("hb2", "Round", "Round hair base"),
            ("hb3", "Tressed", "Tressed hair base"),
            ("hb4", "Arranged", "Arranged hair base"),
            ("bald", "Bald", "No hair")
        ],
        update=update_hair_base
    )
        
    bangs: bpy.props.EnumProperty(
        name="Bangs",
        items=[
            ("none", "None", "Pas de frange"),
            ("boolBangs1", "Shell", "Frange de type 1"),
            ("boolBangs2", "Side", "Frange de type 2"),
            ("boolBangs3", "Heart", "Frange de type 3"),
            ("boolBangs4", "Asymmetrical Heart", "Frange de type 4")
            
        ],
        update=update_hair_base
    )
    
    ear_type: bpy.props.EnumProperty(
        name="Ear Type",
        items=[
            ("human", "Human", "Human ears"),
            ("elfe", "Elfe", "Elfe ears"),
            ("fae", "Fae", "Fae ears")
        ],
        update=update_ear_type  # Appelle la fonction quand l'utilisateur change d'option
    )
    
    earrings: bpy.props.EnumProperty(
        name="Earrings",
        items=[
            ("stud", "Stud", "Stud earrings"),
            ("hoop", "Hoop", "Hoop earrings"),
            ("drop", "Drop", "Drop earrings")
        ],
        update=update_ear_type  # Appelle la fonction lors de la sélection d'une boucle d'oreille
    )
    
    eyelashes: bpy.props.BoolProperty(
        name="Eyelashes",
        description="Enable eyelashes",
        default=True
    )
    
    pupil_texture: bpy.props.EnumProperty(
        name="Pupil Texture",
        items=[("default", "Default", "Default texture"),
               ("cat", "Cat", "Cat-like pupils"),
               ("star", "Star", "Star-shaped pupils")]
    )
    
    mouth_texture: bpy.props.EnumProperty(
        name="Mouth Texture",
        items=[("default", "Default", "Default texture"),
               ("smile", "Smile", "Smiling mouth"),
               ("serious", "Serious", "Serious mouth")]
    )

classes = [BUSTE_PT_CustomizerPanel, BUSTE_CustomizerProperties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.buste_customizer = bpy.props.PointerProperty(type=BUSTE_CustomizerProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.buste_customizer

if __name__ == "__main__":
    register()